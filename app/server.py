# -*- coding: utf-8 -*-
"""
성경말씀 카드 프로그램 - 화면 서버 (추가 설치 없이 파이썬 기본 기능만 사용)
실행: python server.py  →  브라우저가 자동으로 열립니다 (http://localhost:8765)
"""
import json, os, sys, subprocess, threading, webbrowser, uuid, datetime, mimetypes, time, hmac, hashlib, base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote
from make_card import make_card, APP_DIR, RES_DIR, USER_DIR, OUT_DIR, LAST, BG_DIRS
import kakao_auto
_T0 = time.time()
_STARTLOG = []


def tlog(msg):
    _STARTLOG.append(f"{time.time() - _T0:6.2f}s  {msg}")
    try:
        with open(os.path.join(USER_DIR, "startup.log"), "w", encoding="utf-8") as f:
            f.write("\n".join(_STARTLOG))
    except Exception:
        pass


tlog("모듈 로딩 완료")

PORT = 8765
APP_VERSION = "1.0.0"       # 배포할 때마다 올리세요 (version.json 의 version 과 비교)

DATA_DIR = USER_DIR                                   # 지인·이력·프로필 (내 계정 폴더)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)
CONTACTS = os.path.join(DATA_DIR, "contacts.json")
HISTORY = os.path.join(DATA_DIR, "history.json")
VERSES = os.path.join(APP_DIR, "verses.json")
PROFILE = os.path.join(DATA_DIR, "profile.json")
SETTINGS = os.path.join(APP_DIR, "settings.json")   # 서버에서 받는 폴더(업데이트로 갱신됨)
BIBLE = os.path.join(RES_DIR, "bible.json")          # 개역한글 전체 (직접 추가용)
MYVERSES = os.path.join(DATA_DIR, "my_verses.json")  # 사용자가 직접 추가한 구절
BOOK_FULL = {'창':'창세기','출':'출애굽기','레':'레위기','민':'민수기','신':'신명기','수':'여호수아','삿':'사사기','룻':'룻기','삼상':'사무엘상','삼하':'사무엘하','왕상':'열왕기상','왕하':'열왕기하','대상':'역대상','대하':'역대하','스':'에스라','느':'느헤미야','에':'에스더','욥':'욥기','시':'시편','잠':'잠언','전':'전도서','아':'아가','사':'이사야','렘':'예레미야','애':'예레미야애가','겔':'에스겔','단':'다니엘','호':'호세아','욜':'요엘','암':'아모스','옵':'오바댜','욘':'요나','미':'미가','나':'나훔','합':'하박국','습':'스바냐','학':'학개','슥':'스가랴','말':'말라기','마':'마태복음','막':'마가복음','눅':'누가복음','요':'요한복음','행':'사도행전','롬':'로마서','고전':'고린도전서','고후':'고린도후서','갈':'갈라디아서','엡':'에베소서','빌':'빌립보서','골':'골로새서','살전':'데살로니가전서','살후':'데살로니가후서','딤전':'디모데전서','딤후':'디모데후서','딛':'디도서','몬':'빌레몬서','히':'히브리서','약':'야고보서','벧전':'베드로전서','벧후':'베드로후서','요일':'요한일서','요이':'요한이서','요삼':'요한삼서','유':'유다서','계':'요한계시록'}
import re as _re


def lookup(ref):
    """'시23:1' 또는 '시23:1-3' → (본문, 책이름) / 없으면 (None, 오류메시지)"""
    ref = ref.replace(" ", "")
    m = _re.match(r'^([가-힣]+)(\d+):(\d+)(?:-(\d+))?$', ref)
    if not m:
        return None, "형식: 시23:1 또는 시23:1-3 (약칭+장:절)"
    b, c, v1, v2 = m.groups(); v2 = v2 or v1
    if b not in BOOK_FULL:
        return None, f"'{b}' 약칭을 모릅니다. 예: 창 출 시 잠 사 마 요 롬 고전 엡 빌 히 계"
    bible = load(BIBLE, {})
    parts = []
    for vv in range(int(v1), int(v2) + 1):
        k = f"{b}{c}:{vv}"
        if k not in bible:
            return None, f"{k} 절이 없습니다"
        parts.append(bible[k])
    return " ".join(parts), BOOK_FULL[b]


def all_verses():
    """기본 400구절 + 사용자 추가 구절 합치기"""
    base = load(VERSES, {})
    out = {t: [dict(x) for x in items] for t, items in base.items()}
    for t, items in load(MYVERSES, {}).items():
        out.setdefault(t, [])
        for x in items:
            y = dict(x); y["mine"] = True
            out[t].append(y)
    return out   # 개발자(형님)가 정하는 값: 후원계좌, 무료기간 등
SECRET = "mc-RS0Um0pPO7GpXKkH7O7yNpkh7_xBFRM9"     # 키생성기.py 와 반드시 같아야 함


_CACHE = {}


def load(path, default):
    if not os.path.exists(path):
        return default
    if path in (VERSES, BIBLE) and path in _CACHE:      # 구절/성경 파일은 한 번만 읽음
        return _CACHE[path]
    with open(path, encoding="utf-8") as f:
        obj = json.load(f)
    if path in (VERSES, BIBLE):
        _CACHE[path] = obj
    return obj


def save(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def copy_image_to_clipboard(path):
    """윈도우: 이미지를 클립보드에 복사 → 카톡에서 Ctrl+V 로 붙여넣기 가능"""
    if not sys.platform.startswith("win"):
        return False, "윈도우에서만 지원"
    ps = ("Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; "
          f"$img=[System.Drawing.Image]::FromFile('{path}'); "
          "[System.Windows.Forms.Clipboard]::SetImage($img); $img.Dispose()")
    try:
        subprocess.run(["powershell", "-NoProfile", "-STA", "-Command", ps], check=True,
                       capture_output=True, timeout=20)
        return True, ""
    except Exception as e:
        return False, str(e)


SETTINGS_ERR = ""


def settings():
    global SETTINGS_ERR
    d = {"developer": "개발자", "trial_days": 14, "free_mode": True, "price_text": "",
         "ads": True, "ad_url": "", "ad_local": [], "dedication": "", "update_url": "",
         "price_month": "월 3,000원", "price_year": "연 30,000원 (2개월 무료)",
         "donate_url": "", "donate_account": "", "contact": ""}
    try:
        d.update(load(SETTINGS, {}))
        SETTINGS_ERR = ""
    except Exception as e:      # settings.json 이 깨져도 기본값으로 계속 동작
        SETTINGS_ERR = f"settings.json 형식 오류 (따옴표/쉼표 확인): {e}"
    try:
        d["trial_days"] = int(d["trial_days"])
    except Exception:
        d["trial_days"] = 14
    d["error"] = SETTINGS_ERR
    return d


def verify_key(key):
    """키 형식: base64(이름|만료일YYYY-MM-DD|서명)  → 유효하면 (이름, 만료일) 반환"""
    try:
        raw = base64.urlsafe_b64decode(key.strip().encode()).decode("utf-8")
        name, exp, sig = raw.split("|")
        good = hmac.new(SECRET.encode(), f"{name}|{exp}".encode(), hashlib.sha256).hexdigest()[:16]
        if hmac.compare_digest(sig, good):
            return name, exp
    except Exception:
        pass
    return None, None


def license_status():
    prof = load(PROFILE, {})
    if not prof.get("first_run"):
        prof["first_run"] = datetime.date.today().isoformat()
        save(PROFILE, prof)
    st = settings()
    today = datetime.date.today()
    first = datetime.date.fromisoformat(prof["first_run"])
    trial_left = st["trial_days"] - (today - first).days
    name, exp = verify_key(prof.get("license_key", "")) if prof.get("license_key") else (None, None)
    licensed = bool(exp) and datetime.date.fromisoformat(exp) >= today
    free = bool(st.get("free_mode"))
    return {"user": prof.get("user", ""), "first_run": prof["first_run"], "trial_left": trial_left,
            "licensed": licensed, "license_name": name or "", "license_exp": exp or "",
            "active": free or licensed or trial_left > 0, "free_mode": free, "settings": st}


# ── 관리자: 프로그램 업데이트 올리기 (Supabase Storage) ──
# 파일 보관처: GitHub (무료, 멈추지 않음)
GH_OWNER = "apharmga"
GH_REPO = "malssum"
GH_BRANCH = "main"
GH_DIR = "app"
GH_API = f"https://api.github.com/repos/{GH_OWNER}/{GH_REPO}/contents/{GH_DIR}"
GH_RAW = f"https://raw.githubusercontent.com/{GH_OWNER}/{GH_REPO}/{GH_BRANCH}/{GH_DIR}"
APP_FILES = ["server.py", "make_card.py", "kakao_auto.py", "ui.py", "verses.json", "settings.json"]


ADMIN_FILE = os.path.join(DATA_DIR, "admin.json")
ADMIN_DEFAULT_PW = "0089"


def admin_pw_ok(pw):
    saved = load(ADMIN_FILE, {}).get("pw_hash")
    h = hashlib.sha256(("malssum-admin|" + str(pw)).encode()).hexdigest()
    if saved:
        return hmac.compare_digest(saved, h)
    return str(pw) == ADMIN_DEFAULT_PW


def admin_set_pw(new_pw):
    save(ADMIN_FILE, {"pw_hash": hashlib.sha256(("malssum-admin|" + str(new_pw)).encode()).hexdigest()})


def admin_key():
    """형님 PC에만 있는 비밀키 파일 (배포 exe 에는 없음) → 있으면 관리자 기능 활성화"""
    names = ["github_token.txt", "supabase_secret.txt"]
    folders = [USER_DIR, APP_DIR, os.path.join(os.path.expanduser("~"), "Documents", "bible_card")]
    for p in [os.path.join(f, n) for f in folders for n in names]:
        if os.path.exists(p):
            k = open(p, encoding="utf-8-sig").read().strip()
            if k:
                return k
    return ""


def admin_default_folder():
    for p in [os.path.join(os.path.expanduser("~"), "Documents", "bible_card"), APP_DIR]:
        if os.path.exists(os.path.join(p, "server.py")):
            return p
    return APP_DIR


def gh_headers(token=""):
    h = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28",
         "User-Agent": "malssum-app"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def server_manifest():
    """GitHub 에서 manifest 읽기 (API 우선 = 캐시 없음, 실패하면 raw)"""
    import urllib.request, base64 as _b64
    try:
        req = urllib.request.Request(f"{GH_API}/manifest.json?ref={GH_BRANCH}", headers=gh_headers(admin_key()))
        with urllib.request.urlopen(req, timeout=6) as r:
            info = json.loads(r.read().decode("utf-8"))
        return json.loads(_b64.b64decode(info.get("content", "")).decode("utf-8"))
    except Exception:
        pass
    try:
        req = urllib.request.Request(f"{GH_RAW}/manifest.json?t={int(time.time())}",
                                     headers={"Cache-Control": "no-cache", "User-Agent": "malssum-app"})
        with urllib.request.urlopen(req, timeout=6) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return {}


def gh_put(token, name, data, message):
    """GitHub 에 파일 1개 올리기 → (blob_sha, commit_sha)"""
    import urllib.request, urllib.error, base64 as _b64
    url = f"{GH_API}/{name}"
    sha = None
    try:
        req = urllib.request.Request(f"{url}?ref={GH_BRANCH}", headers=gh_headers(token))
        with urllib.request.urlopen(req, timeout=20) as r:
            sha = json.loads(r.read().decode("utf-8")).get("sha")
    except Exception:
        sha = None                      # 새 파일
    body = {"message": message, "content": _b64.b64encode(data).decode("ascii"), "branch": GH_BRANCH}
    if sha:
        body["sha"] = sha
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="PUT",
                                 headers={**gh_headers(token), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            res = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "ignore")[:300]
        raise RuntimeError(f"{name}: GitHub 거부 ({e.code}) {detail}")
    return res.get("content", {}).get("sha", ""), res.get("commit", {}).get("sha", "")


def admin_upload(folder, version, notes):
    return {"ok": False, "error": "파일을 직접 골라서 올리는 방식만 지원합니다."}


def admin_upload_files(files, version, notes):
    """files: [{name, data_b64}] — 고른 파일만 GitHub 에 올리고, 나머지는 기존 manifest 항목 유지"""
    import hashlib
    token = admin_key()
    if not token:
        return {"ok": False, "error": "GitHub 토큰 파일(github_token.txt)이 없습니다."}
    prev = server_manifest().get("files", {})
    out = dict(prev); log = []
    for f in files:
        name = os.path.basename(f.get("name", ""))
        if name not in APP_FILES:
            log.append(f"{name}: 대상 파일이 아니라 건너뜀"); continue
        data = base64.b64decode(f["data_b64"])
        blob_sha, commit_sha = gh_put(token, name, data, f"malssum {version}: {name}")
        entry = {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
        if commit_sha:   # 커밋 고정 주소 → 캐시 문제 없이 정확히 이 버전을 받음
            entry["url"] = f"https://raw.githubusercontent.com/{GH_OWNER}/{GH_REPO}/{commit_sha}/{GH_DIR}/{name}"
        out[name] = entry
        log.append(f"{name}: {len(data):,} bytes 올림")
    if not any(l.endswith("올림") for l in log):
        return {"ok": False, "error": "올린 파일이 없습니다. (server.py 등 대상 파일을 고르세요)"}
    man = {"version": version, "notes": notes,
           "updated_at": datetime.datetime.now().isoformat(timespec="seconds"), "files": out}
    gh_put(token, "manifest.json", json.dumps(man, ensure_ascii=False, indent=1).encode("utf-8"),
           f"malssum {version}: manifest")
    return {"ok": True, "log": log, "version": version}


def app_version_info():
    """실행기가 남겨둔 현재 코드 버전 정보"""
    info = {"app_version": APP_VERSION, "code_version": os.environ.get("MALSSUM_CODE_VERSION", ""),
            "code_notes": os.environ.get("MALSSUM_CODE_NOTES", ""), "source": os.environ.get("MALSSUM_SOURCE", "")}
    try:   # 진단: 설정 파일 위치·존재·폴더 내용
        info["diag"] = f"설정파일: {SETTINGS} ({'있음' if os.path.exists(SETTINGS) else '없음'}) | 오류: {SETTINGS_ERR or '없음'} | 앱폴더 파일: " + ", ".join(sorted(os.listdir(APP_DIR)))[:400]
    except Exception as e:
        info["diag"] = f"진단 실패: {e}"
    return info


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):  # 콘솔 조용히
        pass

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _file(self, path, ctype=None):
        if not os.path.isfile(path):
            self.send_response(404); self.end_headers(); return
        ctype = ctype or mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        try:
            return self._get()
        except Exception as e:
            return self._json({"ok": False, "error": str(e)}, 500)

    def _get(self):
        p = unquote(urlparse(self.path).path)
        if p in ("/", "/index.html"):
            tlog("화면 요청 받음")
            try:
                import importlib, ui
                importlib.reload(ui)
                body = ui.HTML.encode("utf-8")
            except Exception:
                with open(os.path.join(APP_DIR, "index.html"), "rb") as f:
                    body = f.read()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body))); self.send_header("Cache-Control", "no-store"); self.end_headers()
            self.wfile.write(body); return
        if p.startswith("/guide/"):
            safe = os.path.normpath(os.path.join(RES_DIR, "guide", p[len("/guide/"):]))
            if safe.startswith(os.path.join(RES_DIR, "guide")):
                return self._file(safe, "image/gif")
        if p.startswith("/fonts/"):
            safe = os.path.normpath(os.path.join(RES_DIR, p.lstrip("/")))
            if safe.startswith(RES_DIR):
                return self._file(safe)
        if p.startswith("/output/"):
            safe = os.path.normpath(os.path.join(OUT_DIR, p[len("/output/"):]))
            if safe.startswith(OUT_DIR):
                return self._file(safe)
        if p == "/api/ping":
            global LAST_PING
            LAST_PING = time.time()
            return self._json({"ok": True})
        if p == "/api/ads":
            st = settings()
            ads = list(st.get("ad_local") or [])
            url = st.get("ad_url", "")
            if url:
                if "ads" not in _CACHE or time.time() - _CACHE.get("ads_t", 0) > 600:
                    try:
                        import urllib.request
                        with urllib.request.urlopen(url, timeout=3) as r:
                            _CACHE["ads"] = json.loads(r.read().decode("utf-8")); _CACHE["ads_t"] = time.time()
                    except Exception:
                        _CACHE.setdefault("ads", [])
                ads = list(_CACHE.get("ads") or []) + ads
            return self._json({"ok": True, "ads": ads, "show": bool(st.get("ads")) and not license_status()["licensed"]})
        if p == "/api/update":
            return self._json(app_version_info())
        if p == "/api/admin":
            return self._json({"can_upload": bool(admin_key()), "folder": admin_default_folder(), "server": server_manifest()})
        if p == "/api/startlog":
            body = "\n".join(_STARTLOG).encode("utf-8")
            self.send_response(200); self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body); return
        if p == "/api/auto_status":
            return self._json(kakao_auto.STATE)
        if p == "/api/data":
            tlog("데이터 요청 받음")
            history = load(HISTORY, [])
            next_day = (max([h.get("day", 0) for h in history]) + 1) if history else 1
            return self._json({"verses": all_verses(), "contacts": load(CONTACTS, []),
                               "history": history, "next_day": next_day,
                               "windows": sys.platform.startswith("win"),
                               "license": license_status()})
        self.send_response(404); self.end_headers()

    def do_POST(self):
        p = urlparse(self.path).path
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n) or b"{}")
        try:
            if p == "/api/card":
                if not license_status()["active"]:
                    return self._json({"ok": False, "error": "무료 기간이 끝났습니다. [설정·후원] 탭에서 키를 입력해 주세요."})
                verses = all_verses()
                v = verses[body["topic"]][body["idx"]]
                path = make_card(body["topic"], v, int(body["day"]))
                return self._json({"ok": True, "file": os.path.basename(path), "bg": LAST["bg"]})
            if p == "/api/copy":
                ok, err = copy_image_to_clipboard(os.path.join(OUT_DIR, body["file"]))
                return self._json({"ok": ok, "error": err})
            if p == "/api/contacts":
                save(CONTACTS, body["contacts"])
                return self._json({"ok": True})
            if p == "/api/history":
                hist = load(HISTORY, [])
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                for e in body["entries"]:
                    e["id"] = uuid.uuid4().hex[:8]
                    e["sent_at"] = now
                    hist.append(e)
                save(HISTORY, hist)
                return self._json({"ok": True, "history": hist})
            if p == "/api/history_delete":
                hist = [h for h in load(HISTORY, []) if h["id"] != body["id"]]
                save(HISTORY, hist)
                return self._json({"ok": True, "history": hist})
            if p == "/api/open_output":
                if sys.platform.startswith("win"):
                    os.startfile(OUT_DIR)
                return self._json({"ok": True})
            if p == "/api/open_bg":       # 내 배경 폴더 (주제별 폴더 자동 생성)
                root = BG_DIRS[0]
                for t in list(all_verses().keys()) + ["공통"]:
                    os.makedirs(os.path.join(root, t), exist_ok=True)
                if sys.platform.startswith("win"):
                    os.startfile(root)
                return self._json({"ok": True})
            if p == "/api/profile":
                prof = load(PROFILE, {}); prof["user"] = body.get("user", "").strip(); save(PROFILE, prof)
                return self._json({"ok": True, "license": license_status()})
            if p == "/api/activate":
                name, exp = verify_key(body.get("key", ""))
                if not exp:
                    return self._json({"ok": False, "error": "키가 올바르지 않습니다. 다시 확인해 주세요."})
                prof = load(PROFILE, {}); prof["license_key"] = body["key"].strip(); save(PROFILE, prof)
                return self._json({"ok": True, "license": license_status()})
            if p == "/api/auto_start":
                # jobs: [{name, topic, idx, day}] → 카드 없는 것은 여기서 생성
                verses = all_verses()
                jobs = []
                for j in body["jobs"]:
                    if not j.get("file"):
                        v = verses[j["topic"]][j["idx"]]
                        j["file"] = os.path.basename(make_card(j["topic"], v, int(j["day"])))
                    j["path"] = os.path.join(OUT_DIR, j["file"])
                    jobs.append({"name": j["name"], "file": j["path"], "meta": j})
                ok = kakao_auto.start(jobs)
                return self._json({"ok": ok, "error": "" if ok else "이미 발송 중입니다"})
            if p == "/api/auto_stop":
                kakao_auto.STATE["stop"] = True
                return self._json({"ok": True})
            if p == "/api/lookup":
                text, info = lookup(body.get("ref", ""))
                return self._json({"ok": bool(text), "text": text or "", "book": info if text else "", "error": "" if text else info})
            if p == "/api/myverse_add":
                text, book = lookup(body.get("ref", ""))
                if not text:
                    return self._json({"ok": False, "error": book})
                topic = body.get("topic", "").strip() or "내 구절"
                mv = load(MYVERSES, {}); mv.setdefault(topic, [])
                mv[topic].append({"ref": body["ref"].replace(" ", ""), "book": book, "text": text,
                                  "declaration": body.get("declaration", "").strip(), "version": "개역한글",
                                  "id": uuid.uuid4().hex[:8]})
                save(MYVERSES, mv)
                return self._json({"ok": True, "verses": all_verses()})
            if p == "/api/myverse_delete":
                mv = load(MYVERSES, {})
                for t in list(mv.keys()):
                    mv[t] = [x for x in mv[t] if x.get("id") != body["id"]]
                    if not mv[t]:
                        del mv[t]
                save(MYVERSES, mv)
                return self._json({"ok": True, "verses": all_verses()})
            if p == "/api/backup":
                data = {"app": "말씀배달부", "saved_at": datetime.datetime.now().isoformat(timespec="seconds"),
                        "contacts": load(CONTACTS, []), "history": load(HISTORY, []),
                        "my_verses": load(MYVERSES, {}), "user": load(PROFILE, {}).get("user", "")}
                return self._json({"ok": True, "data": data})
            if p == "/api/restore":
                d = body.get("data", {})
                if d.get("app") != "말씀배달부":
                    return self._json({"ok": False, "error": "말씀배달부 백업 파일이 아닙니다."})
                save(CONTACTS, d.get("contacts", [])); save(HISTORY, d.get("history", [])); save(MYVERSES, d.get("my_verses", {}))
                prof = load(PROFILE, {}); prof["user"] = d.get("user") or prof.get("user", ""); save(PROFILE, prof)
                return self._json({"ok": True})
            if p == "/api/admin_login":
                return self._json({"ok": admin_pw_ok(body.get("pw", ""))})
            if p == "/api/admin_setpw":
                if not admin_pw_ok(body.get("old", "")):
                    return self._json({"ok": False, "error": "현재 비밀번호가 틀립니다."})
                if len(str(body.get("new", ""))) != 4:
                    return self._json({"ok": False, "error": "새 비밀번호는 4자리"})
                admin_set_pw(body["new"]); return self._json({"ok": True})
            if p == "/api/admin_upload_files":
                if not admin_pw_ok(body.get("pw", "")):
                    return self._json({"ok": False, "error": "관리자 인증이 필요합니다."})
                try:
                    return self._json(admin_upload_files(body.get("files", []), body.get("version", "").strip(), body.get("notes", "").strip()))
                except Exception as e:
                    return self._json({"ok": False, "error": f"업로드 실패: {e}"})
            if p == "/api/admin_upload":
                if not admin_pw_ok(body.get("pw", "")):
                    return self._json({"ok": False, "error": "관리자 인증이 필요합니다."})
                try:
                    return self._json(admin_upload(body.get("folder") or admin_default_folder(), body.get("version", "").strip(), body.get("notes", "").strip()))
                except Exception as e:
                    return self._json({"ok": False, "error": f"업로드 실패: {e}"})
            if p == "/api/restart":
                self._json({"ok": True})
                def _re():
                    time.sleep(0.3)
                    try:
                        if getattr(sys, "frozen", False):
                            open(os.path.join(APP_DIR, ".restart"), "w").close()     # 실행기가 보고 재실행
                        else:
                            subprocess.Popen([sys.executable, os.path.abspath(__file__)], close_fds=True)
                    except Exception:
                        pass
                    srv_shutdown()
                threading.Thread(target=_re, daemon=True).start()
                return
            if p == "/api/quit":
                self._json({"ok": True})
                threading.Thread(target=self.server.shutdown, daemon=True).start()
                return
            if p == "/api/verses":  # 구절 편집 저장
                save(VERSES, body["verses"])
                return self._json({"ok": True})
        except Exception as e:
            return self._json({"ok": False, "error": str(e)}, 500)
        self.send_response(404); self.end_headers()


LAST_PING = None


def open_app_window(url):
    """Edge/Chrome '앱 모드'(주소창 없는 창)로 열기. 없으면 일반 브라우저."""
    cands = []
    for env in ("PROGRAMFILES(X86)", "PROGRAMFILES", "LOCALAPPDATA"):
        root = os.environ.get(env)
        if root:
            cands += [os.path.join(root, "Microsoft", "Edge", "Application", "msedge.exe"),
                      os.path.join(root, "Google", "Chrome", "Application", "chrome.exe")]
    for exe in cands:
        if os.path.exists(exe):
            # 별도 프로필 없이 실행 → 이미 켜진 브라우저를 재사용해 1초 안에 창이 뜸
            subprocess.Popen([exe, f"--app={url}", "--window-size=1400,900", "--no-first-run"])
            tlog("브라우저 창 실행 요청")
            return
    webbrowser.open(url)


def watchdog(srv):
    """화면 창이 닫히면(핑이 끊기면) 프로그램 자동 종료"""
    start = time.time()
    while True:
        time.sleep(3)
        if LAST_PING is None:
            if time.time() - start > 90:   # 창이 아예 안 열린 경우
                break
        elif time.time() - LAST_PING > 15:
            break
    srv.shutdown()


_SRV = {"srv": None}


def srv_shutdown():
    if _SRV["srv"]:
        threading.Thread(target=_SRV["srv"].shutdown, daemon=True).start()


def bind_server():
    """8765부터 차례로 시도. 이미 켜진 우리 프로그램이면 종료시키고 재시도, 윈도우가 막은 번호면 즉시 다음 번호로."""
    global PORT
    import socket, urllib.request
    for port in [8765, 8766, 8767, 8770, 8780, 8790, 8800, 8850, 8900, 9000, 9100, 9200, 18765, 28765]:
        for attempt in range(3):
            try:
                srv = HTTPServer(("127.0.0.1", port), H)
                PORT = port
                tlog(f"주소 {port} 확보")
                return srv
            except OSError:
                try:      # 누가 쓰고 있나 0.2초만 확인 → 응답 없으면(윈도우가 막은 번호) 바로 다음 번호
                    with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                        pass
                except Exception:
                    tlog(f"주소 {port} 사용불가 → 다음")
                    break
                try:      # 우리 프로그램이 켜져 있으면 종료 요청
                    urllib.request.urlopen(urllib.request.Request(f"http://127.0.0.1:{port}/api/quit", data=b"{}",
                                           headers={"Content-Type": "application/json"}), timeout=1)
                except Exception:
                    break
                time.sleep(1.2)
    srv = HTTPServer(("127.0.0.1", 0), H)
    PORT = srv.server_address[1]
    tlog(f"임의 주소 {PORT} 확보")
    return srv


if __name__ == "__main__":
    tlog("시작")
    HTTPServer.allow_reuse_address = True
    srv = bind_server()
    _SRV["srv"] = srv
    url = f"http://localhost:{PORT}"
    print("말씀배달부 실행 중:", url)
    if not os.environ.get("MALSSUM_NO_WINDOW"):
        threading.Timer(0.2, lambda: open_app_window(url)).start()
    else:
        globals()["LAST_PING"] = time.time()          # 창은 이미 떠 있으므로 감시 타이머 초기화
    threading.Thread(target=watchdog, args=(srv,), daemon=True).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    srv.server_close()
