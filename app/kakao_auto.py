# -*- coding: utf-8 -*-
"""
PC 카카오톡 완전자동 발송
 - 카톡 메인창 → 친구검색(Ctrl+F) → 이름 입력 → Enter(대화방 열기) → 이미지 붙여넣기(Ctrl+V) → Enter(전송) → Esc(닫기)
 - 발송 중에는 마우스/키보드를 건드리면 안 됩니다.
"""
import os, sys, time, random, subprocess, threading

WIN = sys.platform.startswith("win")
HAVE = None
pyautogui = pyperclip = None


def _load_gui():
    """자동발송을 실제로 시작할 때만 pyautogui 를 불러옴 (프로그램 시작 속도 개선)"""
    global pyautogui, pyperclip, HAVE
    if HAVE is not None:
        return HAVE
    try:
        import pyautogui as _pa, pyperclip as _pc
        _pa.FAILSAFE = True   # 마우스를 화면 왼쪽 위 모서리로 밀면 즉시 중단
        _pa.PAUSE = 0.15
        pyautogui, pyperclip, HAVE = _pa, _pc, True
    except Exception:
        HAVE = False
    return HAVE

STATE = {"running": False, "stop": False, "log": [], "done": [], "failed": [], "current": "", "total": 0, "index": 0}


def log(msg):
    STATE["log"].append(time.strftime("%H:%M:%S ") + msg)
    if len(STATE["log"]) > 200:
        STATE["log"] = STATE["log"][-200:]


def clip_image(path):
    ps = ("Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; "
          f"$img=[System.Drawing.Image]::FromFile('{path}'); "
          "[System.Windows.Forms.Clipboard]::SetImage($img); $img.Dispose()")
    subprocess.run(["powershell", "-NoProfile", "-STA", "-Command", ps], check=True, capture_output=True, timeout=20)


# ── 윈도우 창 찾기 (윈도우 기본 API 직접 사용: 한글 제목도 정확히 읽음) ──
if WIN:
    import ctypes
    from ctypes import wintypes
    u32 = ctypes.windll.user32
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)


def list_windows(visible_only=True):
    """[(hwnd, 제목, 클래스명)]"""
    out = []
    if not WIN:
        return out
    def cb(hwnd, _):
        if (not visible_only) or u32.IsWindowVisible(hwnd):
            n = u32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(n + 1); u32.GetWindowTextW(hwnd, buf, n + 1)
            cls = ctypes.create_unicode_buffer(256); u32.GetClassNameW(hwnd, cls, 256)
            if buf.value.strip():
                out.append((hwnd, buf.value.strip(), cls.value))
        return True
    u32.EnumWindows(EnumWindowsProc(cb), 0)
    return out


def kakao_windows():
    return [w for w in list_windows() if w[2].startswith("EVA_")]   # 카카오톡 창들은 클래스명이 EVA_ 로 시작


def _match_main(ws):
    for hwnd, t, c in ws:
        if t == "카카오톡":
            return hwnd
    for hwnd, t, c in ws:          # 제목이 조금 다른 버전 대비
        if "카카오톡" in t or "KakaoTalk" in t:
            return hwnd
    return None


def find_main():
    # 1) 화면에 보이는 창
    h = _match_main(kakao_windows())
    if h:
        return h
    # 2) 트레이로 숨겨진 창 → 화면에 띄우기
    hidden = [w for w in list_windows(False) if w[2].startswith("EVA_")]
    h = _match_main(hidden)
    if h:
        log("카톡이 숨겨져 있어 화면에 띄웁니다.")
        u32.ShowWindow(h, 9); time.sleep(1.0)
        return h
    # 3) 카톡이 꺼져 있음 → 실행 (자동로그인 설정 필요)
    for env in ("PROGRAMFILES(X86)", "PROGRAMFILES", "LOCALAPPDATA"):
        root = os.environ.get(env)
        exe = os.path.join(root or "", "Kakao", "KakaoTalk", "KakaoTalk.exe")
        if root and os.path.exists(exe):
            log("PC카톡이 꺼져 있어 실행합니다… (최대 40초 대기)")
            subprocess.Popen([exe])
            t0 = time.time()
            while time.time() - t0 < 40:
                time.sleep(2)
                h = _match_main(kakao_windows())
                if h:
                    time.sleep(2); return h
            log("카톡이 뜨긴 했는데 로그인 창일 수 있습니다. 로그인 후 다시 시도하세요.")
            return None
    return None


def activate(hwnd):
    _load_gui()
    try:
        u32.ShowWindow(hwnd, 9)          # SW_RESTORE
        # 윈도우가 앞으로 가져오기를 막는 것 방지 (키 입력 없이 스레드 연결 방식)
        fg = u32.GetForegroundWindow()
        cur = ctypes.windll.kernel32.GetCurrentThreadId()
        tgt = u32.GetWindowThreadProcessId(fg, None) if fg else 0
        if tgt and tgt != cur:
            u32.AttachThreadInput(cur, tgt, True)
        u32.SetForegroundWindow(hwnd)
        u32.BringWindowToTop(hwnd)
        if tgt and tgt != cur:
            u32.AttachThreadInput(cur, tgt, False)
    except Exception:
        pass
    time.sleep(0.7)


def wait_chat(name, timeout=6):
    t0 = time.time()
    while time.time() - t0 < timeout:
        for hwnd, t, c in kakao_windows():
            if t != "카카오톡" and (t == name or t.startswith(name)):
                return hwnd
        time.sleep(0.3)
    return None


def close_new_windows(before):
    for hwnd, t, c in kakao_windows():
        if hwnd not in before and t != "카카오톡":
            u32.PostMessageW(hwnd, 0x0010, 0, 0)   # WM_CLOSE


def send_one(name, image_path, delay):
    """한 사람에게 카드 1장 전송. 성공 True / 실패 False"""
    main = find_main()
    if not main:
        log("카카오톡 메인창을 찾지 못했습니다. PC카톡을 로그인해서 켜두세요.")
        return False
    before = {w[0] for w in kakao_windows()}

    # 1. 카톡 창을 화면에 띄움 (꺼짐/최소화/트레이 모두 처리)
    activate(main)
    time.sleep(0.5)
    # 2. Ctrl+F → 검색칸의 기존 글자 지우기 → 이름 붙여넣기 → Enter
    pyautogui.hotkey("ctrl", "f"); time.sleep(0.8)
    pyautogui.press("end")
    pyautogui.press("backspace", presses=30, interval=0.02)
    time.sleep(0.2)
    pyperclip.copy(name)
    pyautogui.hotkey("ctrl", "v"); time.sleep(1.3)
    # 엉뚱한 창(친구 추가 등)이 떴으면 Enter 누르지 않고 닫고 실패 처리
    odd = [(h_, t) for h_, t, c in kakao_windows() if h_ not in before and t != "카카오톡" and t != name]
    if odd:
        for h_, t in odd:
            u32.PostMessageW(h_, 0x0010, 0, 0)
        log(f"[{name}] 검색 대신 '{odd[0][1]}' 창이 떴습니다. (Ctrl+F가 검색으로 먹히지 않음)")
        return False
    pyautogui.press("enter")
    chat = wait_chat(name, 5)
    if not chat:
        close_new_windows(before)
        log(f"[{name}] 일치하는 친구가 없어 대화창이 열리지 않았습니다. 카톡 친구 이름이 '{name}'과 정확히 같은지 확인하세요.")
        return False
    # 3. 대화창에 이미지 붙여넣기 → Enter(전송)
    activate(chat)
    clip_image(image_path); time.sleep(0.5)
    pyautogui.hotkey("ctrl", "v"); time.sleep(1.5)
    pyautogui.press("enter"); time.sleep(1.5)
    # 4. 대화창 닫기 (대화창에서의 Esc는 대화창만 닫힘)
    pyautogui.press("esc"); time.sleep(0.4)
    close_new_windows(before)
    log(f"[{name}] 전송 완료")
    time.sleep(delay)
    return True


def run(jobs, min_delay=4, max_delay=9):
    """jobs: [{"name":..., "file":절대경로, ...}]"""
    STATE.update({"running": True, "stop": False, "log": [], "done": [], "failed": [], "total": len(jobs), "index": 0})
    if not WIN or not _load_gui():
        log("윈도우 + pyautogui 가 필요합니다. 1_처음한번만_설치.bat 을 다시 실행하세요.")
        STATE["running"] = False
        return
    log(f"자동 발송 시작: {len(jobs)}명. 마우스/키보드를 건드리지 마세요. (긴급중단: 마우스를 화면 왼쪽 위 모서리로)")
    try:
        for i, j in enumerate(jobs):
            if STATE["stop"]:
                log("사용자가 중단했습니다.")
                break
            STATE["index"] = i + 1
            STATE["current"] = j["name"]
            try:
                ok = send_one(j["name"], j["file"], random.uniform(min_delay, max_delay))
            except pyautogui.FailSafeException:
                log("긴급중단(마우스 모서리) 감지")
                break
            except Exception as e:
                log(f"[{j['name']}] 오류: {e}")
                ok = False
            (STATE["done"] if ok else STATE["failed"]).append(j)
            if not ok:
                log(f"※ 발송 중단: '{j['name']}' 문제를 해결한 뒤 다시 시작하세요. (앞서 성공한 사람은 기록됨)")
                break
    finally:
        STATE["running"] = False
        STATE["current"] = ""
        log(f"끝. 성공 {len(STATE['done'])}명 / 실패 {len(STATE['failed'])}명")


def start(jobs):
    if STATE["running"]:
        return False
    threading.Thread(target=run, args=(jobs,), daemon=True).start()
    return True
