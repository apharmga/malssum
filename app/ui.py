# -*- coding: utf-8 -*-
"""말씀배달부 화면 (index.html 을 py 로 감싼 것). 화면을 고칠 땐 index.html 을 고친 뒤 이 파일을 다시 생성합니다."""
HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>말씀배달부</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
@font-face{font-family:"NM";src:url(/fonts/NanumMyeongjo-Regular.ttf);font-weight:400}
@font-face{font-family:"NM";src:url(/fonts/NanumMyeongjo-Bold.ttf);font-weight:700}
@font-face{font-family:"NM";src:url(/fonts/NanumMyeongjo-ExtraBold.ttf);font-weight:800}
@font-face{font-family:"NP";src:url(/fonts/NanumPenScript-Regular.ttf)}
:root{
  --cream:#F8F4EC;--paper:#FFFFFF;--ink:#2B2924;--olive:#5E7A4A;--olive-deep:#4A6238;
  --sage:#E4EADB;--line:#E6E0D4;--gray:#8B867C;--warn:#B7532F;--sky:#EEF3F8;
}
*{box-sizing:border-box}
html,body{margin:0;background:var(--cream);color:var(--ink);font-family:"Malgun Gothic","Apple SD Gothic Neo",sans-serif;font-size:15px;line-height:1.55}
button{font-family:inherit;font-size:15px;cursor:pointer;border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:8px;padding:9px 14px}
button:hover{border-color:var(--olive)}
button.primary{background:var(--olive);border-color:var(--olive);color:#fff;font-weight:700}
button.primary:hover{background:var(--olive-deep)}
button.ghost{background:transparent}
button:disabled{opacity:.45;cursor:not-allowed}
input,select,textarea{font-family:inherit;font-size:15px;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink)}
input:focus,select:focus,textarea:focus,button:focus-visible{outline:2px solid var(--olive);outline-offset:1px}

header{display:flex;align-items:center;gap:28px;padding:14px 28px;border-bottom:1px solid var(--line);background:var(--paper);position:sticky;top:0;z-index:5}
header h1{font-family:"NM";font-weight:800;font-size:22px;margin:0;letter-spacing:.02em}
header h1 small{font-family:"NP";font-weight:400;color:var(--olive);font-size:22px;margin-left:8px}
nav{display:flex;gap:4px}
nav button{border:none;background:transparent;padding:8px 14px;border-radius:999px;color:var(--gray);font-weight:700}
nav button.on{background:var(--sage);color:var(--olive-deep)}
header .spacer{flex:1}
header .stat{color:var(--gray);font-size:13px}

main{padding:20px 28px 60px}
.page{display:none}.page.on{display:block}

/* ── 카드 만들기 ── */
.work{display:grid;grid-template-columns:150px minmax(380px,1fr) 400px;gap:20px;align-items:start}
.topics{display:flex;flex-direction:column;gap:4px;position:sticky;top:76px}
.topics button{text-align:left;border:none;background:transparent;padding:8px 12px;border-radius:8px;font-weight:700;color:var(--gray)}
.topics button.on{background:var(--paper);color:var(--olive-deep);box-shadow:inset 3px 0 0 var(--olive)}
.topics button .n{float:right;font-weight:400;font-size:12px}

.panel{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:18px 20px}
.panel h2{font-family:"NM";font-weight:800;font-size:18px;margin:0 0 12px}
.verse{padding:14px 16px;border:1px solid var(--line);border-radius:10px;margin-bottom:10px;cursor:pointer;display:grid;grid-template-columns:1fr auto;gap:8px 12px;align-items:start}
.verse:hover{border-color:var(--olive)}
.verse.on{border-color:var(--olive);background:var(--sage)}
.verse .ref{font-weight:700;color:var(--olive-deep)}
.verse .txt{font-family:"NM";font-weight:700;font-size:18px;line-height:1.85;grid-column:1/-1;letter-spacing:-.005em;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
.verse .decl{grid-column:1/-1;color:var(--gray);font-size:14px;line-height:1.7}
.verse .decl::before{content:"선포  ";color:var(--olive);font-family:"NP";font-size:16px}
.verse .sent{font-size:12px;color:var(--gray);white-space:nowrap}
.verse .sent b{color:var(--warn)}

.make{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:14px;padding:12px 14px;background:var(--sage);border-radius:10px;position:sticky;top:76px;z-index:2}
.make label{color:var(--gray)}
.make input[type=number]{width:90px;font-size:18px;font-weight:700;text-align:center}

.preview{position:sticky;top:76px}
.preview .img{background:var(--cream);border-radius:10px;min-height:280px;display:flex;align-items:center;justify-content:center;color:var(--gray);overflow:hidden}
.preview img{width:100%;display:block;border-radius:10px}
.contacts{max-height:260px;overflow:auto;border:1px solid var(--line);border-radius:10px;padding:6px;margin:10px 0}
.contacts label{display:flex;align-items:center;gap:10px;padding:7px 8px;border-radius:6px;cursor:pointer}
.contacts label:hover{background:var(--cream)}
.contacts label.dup{color:var(--warn)}
.contacts label .g{margin-left:auto;font-size:12px;color:var(--gray)}
.contacts input{width:18px;height:18px}
.row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.row.between{justify-content:space-between}
.hint{color:var(--gray);font-size:13px;margin-top:8px}
.steps{background:var(--sage);border-radius:10px;padding:12px 14px;margin-top:12px;font-size:14px}
.steps b{color:var(--olive-deep)}

.qsel{padding:5px 6px;font-size:14px;max-width:260px}
.plan{border:1px solid var(--line);background:var(--paper)}.plan:hover{border-color:var(--olive)}.plan.on{border:2px solid var(--olive);background:var(--sage);color:var(--olive-deep)}
/* ── 지인 ── */
.people{display:grid;grid-template-columns:1fr 1fr;gap:20px}
table{width:100%;border-collapse:collapse}
th,td{padding:10px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:middle}
th{color:var(--gray);font-weight:700;font-size:13px}
td .del{border:none;color:var(--gray);padding:4px 8px}
td .del:hover{color:var(--warn)}

/* ── 이력 ── */
.filters{display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.tag{display:inline-block;background:var(--sage);color:var(--olive-deep);border-radius:999px;padding:2px 10px;font-size:12px;font-weight:700}

/* ── 개별발송 모달 ── */
.modal{position:fixed;inset:0;background:rgba(43,41,36,.45);display:none;align-items:center;justify-content:center;z-index:20}
.modal.on{display:flex}
.box{background:var(--paper);border-radius:16px;padding:28px 32px;width:480px;max-width:92vw;text-align:center}
.box .who{font-family:"NM";font-weight:800;font-size:34px;margin:6px 0 4px}
.box .prog{color:var(--gray);font-size:13px}
.box .steps{text-align:left}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:var(--ink);color:#fff;padding:10px 18px;border-radius:999px;font-size:14px;opacity:0;transition:opacity .2s;pointer-events:none;z-index:30}
.toast.on{opacity:1}
@media (max-width:1100px){.work{grid-template-columns:130px 1fr}.preview{grid-column:1/-1;position:static}.people{grid-template-columns:1fr}}
</style>
</head>
<body>
<header>
  <h1>말씀배달부 <small>믿음의 선포</small></h1>
  <nav>
    <button class="on" data-p="make">카드 만들기</button>
    <button data-p="custom">맞춤 발송</button>
    <button data-p="people">지인 관리</button>
    <button data-p="hist">발송 이력</button>
    <button data-p="set" id="tabSet">설정</button>
  </nav>
  <div class="spacer"></div>
  <div class="stat" id="stat"></div>
  <button class="ghost" id="btnAdmin" style="color:var(--gray)">관리자</button>
  <button class="ghost" id="btnGuide">사용법</button>
  <button class="ghost" id="btnQuit" style="color:var(--gray)">종료</button>
</header>

<main>
<!-- ───────── 카드 만들기 ───────── -->
<section class="page on" id="p-make">
  <div id="lock" style="display:none;background:#F6E4DC;color:#B7532F;border-radius:10px;padding:14px 18px;margin-bottom:16px;font-weight:700"></div>
  <div class="work">
    <div class="topics" id="topics"></div>
    <div class="panel">
      <h2 id="topicTitle">주제를 고르세요</h2>
      <div class="make" id="make" style="display:none">
        <b id="selRef" style="color:var(--olive-deep)"></b><label>몇 일차</label><input type="number" id="day" min="1" value="1">
        <button class="primary" id="btnMake">카드 만들기</button>
        <span class="hint" id="makeMsg"></span>
      </div>
      <div id="verses"></div>
      <details id="addBox" style="margin-top:14px;border-top:1px dashed var(--line);padding-top:12px">
        <summary style="cursor:pointer;font-weight:700;color:var(--olive-deep)">＋ 이 주제에 구절 직접 추가</summary>
        <div class="row" style="margin-top:10px"><input id="aRef" placeholder="구절 주소 (예: 시23:1 또는 롬8:28-29)" style="width:260px"><button id="aLook">본문 불러오기</button><span class="hint" id="aMsg"></span></div>
        <div id="aText" class="hint" style="margin:8px 0;font-family:NM;font-size:16px;color:var(--ink)"></div>
        <div class="row"><input id="aDecl" placeholder="믿음의 선포문 (예: 나는 ~합니다.)" style="flex:1"><button class="primary" id="aAdd">추가</button></div>
        <p class="hint">약칭: 창 출 레 민 신 수 삿 룻 삼상 삼하 왕상 왕하 대상 대하 스 느 에 욥 시 잠 전 아 사 렘 애 겔 단 호 욜 암 옵 욘 미 나 합 습 학 슥 말 마 막 눅 요 행 롬 고전 고후 갈 엡 빌 골 살전 살후 딤전 딤후 딛 몬 히 약 벧전 벧후 요일 요이 요삼 유 계</p>
      </details>
    </div>
    <div class="panel preview">
      <h2>미리보기 · 보내기</h2>
      <div class="img" id="cardImg">주제 → 구절 → 카드 만들기 순서로 진행하세요</div>
      <div id="sendBox" style="display:none">
        <div class="row between" style="margin-top:12px">
          <b>받을 사람</b>
          <span class="row"><button class="ghost" id="selAll">전체 선택</button><button class="ghost" id="selNone">해제</button></span>
        </div>
        <input id="cFind" placeholder="이름 검색 (Ctrl+F)" style="width:100%;margin-top:8px">
        <div class="contacts" id="cList"></div>
        <div class="row">
          <button class="primary" id="btnStep">한 명씩 보내기 시작</button>
          <button class="primary" id="btnAuto" style="background:#8A5A2B;border-color:#8A5A2B">카톡 자동 발송</button>
          <button id="btnCopy">카드 복사</button>
          <button id="btnMark">보냈음으로 기록만</button>
        </div>
        <div class="steps">
          <b>한 명씩 보내기</b>: 이름이 뜨면 카톡에서 그 사람 대화방 열고 <b>Ctrl+V → Enter</b>, 프로그램에서 <b>보냈음</b> 클릭. 카드는 자동으로 복사되어 있습니다.<br>
          <b>카톡 자동 발송</b>: PC카톡을 프로그램이 직접 조작해 검색→대화방→붙여넣기→전송까지 합니다. 발송 중 마우스·키보드 금지.<br>
          <b>카드 복사</b>: 카톡 '나에게 보내기'에 붙여넣고 <b>전달</b>로 여러 명 보내는 방식일 때 사용 → 보낸 뒤 '보냈음으로 기록만' 클릭.
        </div>
        <div class="hint"><button class="ghost" id="btnFolder">카드 저장 폴더 열기</button></div>
      </div>
    </div>
  </div>
</section>

<!-- ───────── 맞춤 발송 ───────── -->
<section class="page" id="p-custom">
  <div class="panel">
    <h2>맞춤 발송 <span class="hint">사람마다 다른 말씀을 정해두고 한 번에 보냅니다</span></h2>
    <div class="row" style="margin-bottom:12px">
      <button id="qSame">체크한 사람 모두 첫 줄과 같은 말씀으로</button>
      <button id="qClear" class="ghost">비우기</button>
      <input id="qFind" placeholder="이름 검색 (Ctrl+F)" style="width:180px">
      <span class="spacer" style="flex:1"></span>
      <button class="primary" id="qStart" style="font-size:16px;padding:11px 22px">한 명씩 보내기</button>
      <button class="primary" id="qAuto" style="font-size:16px;padding:11px 22px;background:#8A5A2B;border-color:#8A5A2B">카톡 자동 발송</button>
    </div>
    <table><thead><tr><th><input type="checkbox" id="qAll"></th><th>이름</th><th>메모</th><th>주제</th><th>구절</th><th>일차</th><th>이 구절</th></tr></thead><tbody id="qTable"></tbody></table>
    <p class="hint">지인 관리 탭에 적어둔 사람이 여기 나옵니다. 메모(상황)를 보고 주제를 고르면 편합니다.</p>
  </div>
</section>

<!-- ───────── 지인 관리 ───────── -->
<section class="page" id="p-people">
  <div class="people">
    <div class="panel">
      <h2>지인 추가</h2>
      <div class="row" style="margin-bottom:10px">
        <input id="cName" placeholder="이름 (카톡 이름과 같게)" style="flex:1">
        <select id="cGroup"><option>가족</option><option>교회</option><option>직장</option><option>친구</option><option>기타</option></select>
      </div>
      <div class="row"><input id="cMemo" placeholder="메모 (예: 수술 회복 중, 취업 준비)" style="flex:1"><button class="primary" id="btnAdd">추가</button></div>
      <p class="hint">최대 30명 권장. 이름은 카톡 친구 이름과 똑같이 적어두면 찾기 편합니다.</p>
    </div>
    <div class="panel">
      <h2>지인 목록 <span class="tag" id="cCount"></span></h2>
      <table><thead><tr><th>이름</th><th>그룹</th><th>메모</th><th>받은 카드</th><th>마지막</th><th></th></tr></thead><tbody id="cTable"></tbody></table>
    </div>
  </div>
</section>

<!-- ───────── 발송 이력 ───────── -->
<section class="page" id="p-hist">
  <div class="panel">
    <h2>발송 이력 <span class="tag" id="hCount"></span></h2>
    <div class="filters">
      <input id="fName" placeholder="이름 검색" style="width:160px">
      <select id="fTopic"><option value="">모든 주제</option></select>
      <input id="fRef" placeholder="구절 (예: 살전5:18)" style="width:160px">
      <button class="ghost" id="fClear">초기화</button>
    </div>
    <table><thead><tr><th>보낸 날짜</th><th>받은 사람</th><th>일차</th><th>주제</th><th>구절</th><th>파일</th><th></th></tr></thead><tbody id="hTable"></tbody></table>
  </div>
</section>
<!-- ───────── 설정·후원 ───────── -->
<section class="page" id="p-set">
  <div class="people">
    <div class="panel">
      <h2>내 정보</h2>
      <div class="row" style="margin-bottom:10px"><label style="width:90px;color:var(--gray)">사용자 이름</label><input id="sUser" style="flex:1"><button id="sUserSave">저장</button></div>
      <div class="row" style="margin-bottom:6px"><label style="width:90px;color:var(--gray)">사용 시작일</label><span id="sFirst"></span></div>
      <div class="row" style="margin-bottom:6px"><label style="width:90px;color:var(--gray)">버전</label><span id="sVer"></span> <span class="hint">(실행할 때마다 자동 업데이트)</span><button class="ghost" id="sUpdChk" style="display:none"></button></div>
      <div class="row" style="margin-bottom:6px"><label style="width:90px;color:var(--gray)">진단</label><span id="sDiag" class="hint" style="font-size:12px;word-break:break-all"></span></div>
      <div class="row" style="margin-bottom:6px"><label style="width:90px;color:var(--gray)">이용 상태</label><span id="sStatus"></span></div>
      <p class="hint">기록(지인·발송이력)은 이 컴퓨터의 내 계정 폴더에 저장됩니다.</p>
      <p class="hint">성경 본문: 『성경전서 개역한글판』(대한성서공회) — 저작재산권 보호기간 만료본을 원문 그대로 사용합니다.</p>
      <h2 style="margin-top:18px">사용법</h2>
      <div class="row"><button id="btnGuide2">사용법 보기 (움직이는 그림)</button></div>
      <h2 style="margin-top:18px">백업 · 복원</h2>
      <div class="row"><button id="bkDown">백업 파일 저장</button><button class="ghost" id="bkUpBtn">백업 파일 불러오기</button><input type="file" id="bkUp" accept=".json" style="display:none"></div>
      <p class="hint">지인·발송 이력·직접 추가한 구절을 파일 하나로 저장합니다. PC를 바꿀 때 새 PC에서 "불러오기" 하세요. (현재 기록은 백업 파일 내용으로 교체됩니다)</p>
      <div class="row" style="margin-top:8px"><button id="sBg">내 배경 사진 폴더 열기</button><button class="ghost" id="sOut">만든 카드 폴더 열기</button><button class="ghost" id="sLog">시작 기록 보기</button></div>
      <pre id="sLogBox" style="display:none;background:var(--cream);border-radius:8px;padding:10px;font-size:12px;white-space:pre-wrap"></pre>
      <p class="hint">내 배경 사진 폴더의 주제 폴더(감사, 위로…)에 사진을 넣으면 기본 사진 대신 내 사진이 사용됩니다.</p>
    </div>
    <div class="panel">
      <h2 id="sDonateTitle">이용권 · 후원</h2>
      <div id="sDonate"></div>
      <div class="row" id="sKeyRow" style="margin-top:14px"><input id="sKey" placeholder="후원자 코드를 여기에 붙여넣기 (광고 제거)" style="flex:1"><button class="primary" id="sKeyBtn">등록</button></div>
      <p class="hint" id="sKeyMsg">후원해 주신 분께는 광고가 표시되지 않는 후원자 코드를 보내드립니다.</p>
      <h2 style="margin-top:22px">이용 안내</h2>
      <ul class="hint" style="margin:0;padding-left:18px;line-height:1.8">
        <li>이 프로그램은 윈도우 PC와 PC 카카오톡(로그인 상태)에서 동작합니다.</li>
        <li><b>카톡 자동 발송</b>은 PC 카카오톡 화면을 대신 조작하는 방식이라, 카카오톡 업데이트나 PC 환경에 따라 동작이 달라질 수 있습니다. 이 경우 <b>한 명씩 보내기</b>(카드 복사 → 붙여넣기)를 이용해 주세요.</li>
        <li>지인 이름은 카카오톡 친구 이름과 정확히 같아야 자동 발송이 됩니다.</li>
        <li>발송 중에는 마우스·키보드를 사용하지 마세요. 긴급 중단은 마우스를 화면 왼쪽 위 모서리로 이동.</li>
        <li>모든 기록은 사용자 PC에만 저장되며 외부로 전송되지 않습니다.</li>
        <li id="liLicense">이용권은 후원 확인 후 키로 발급되며, 발급된 이용권은 환불되지 않습니다. 프로그램 문제로 이용이 불가능한 경우 문의처로 연락 주시면 기간 연장 등으로 도와드립니다.</li>
        <li id="liFree" style="display:none">이 프로그램은 무료로 자유롭게 사용할 수 있으며, 후원은 전적으로 자발적입니다. 후원금은 환불되지 않습니다.</li>
      </ul>
      <div id="adBox" style="display:none;margin-top:18px;border-top:1px dashed var(--line);padding-top:14px">
        <div class="hint" style="margin-bottom:8px">광고</div>
        <div id="adList" style="display:flex;flex-direction:column;gap:10px"></div>
      </div>
      <p id="dedication" class="hint" style="display:none;margin:26px 0 0;text-align:right;line-height:1.8"></p>
    </div>
  </div>
</section>
</main>
<div class="modal" id="welcome"><div class="box">
  <div style="font-family:NP;font-size:26px;color:var(--olive)">- 믿음의 선포 -</div>
  <div class="who" style="font-size:26px">말씀배달부에 오신 것을 환영합니다</div>
  <p style="color:var(--gray)">매일 성경 말씀 카드를 만들어 소중한 분들께 보내보세요.<br>먼저 사용하실 이름을 알려주세요.</p>
  <input id="wName" placeholder="이름" style="width:70%;font-size:18px;text-align:center">
  <div class="row" style="justify-content:center;margin-top:16px"><button class="primary" id="wGo" style="font-size:17px;padding:12px 28px">시작하기</button></div>
  <p class="hint" id="wTrial"></p>
</div></div>

<div class="modal" id="modal"><div class="box">
  <div class="prog" id="mProg"></div>
  <div class="who" id="mWho"></div>
  <div id="mInfo" class="hint" style="margin-bottom:8px"></div>
  <img id="mImg" style="display:none;height:220px;border-radius:8px;margin:0 auto 10px">
  <div class="steps" id="mSteps">카드가 복사되었습니다.<br>카톡에서 <b>이 사람 대화방</b>을 열고 <b>Ctrl+V</b> 후 <b>Enter</b>로 전송하세요.</div>
  <div class="row" style="justify-content:center;margin-top:18px">
    <button class="primary" id="mDone" style="font-size:17px;padding:12px 26px">보냈음 → 다음</button>
    <button id="mSkip">건너뛰기</button>
    <button class="ghost" id="mRecopy">다시 복사</button>
    <button class="ghost" id="mStop">중단</button>
  </div>
</div></div>
<div class="modal" id="autoM"><div class="box" style="width:560px">
  <div class="who" style="font-size:24px">카톡 자동 발송</div>
  <div id="aWarn" class="steps" style="text-align:left">
    <b>시작 전 확인</b><br>1) PC 카카오톡이 <b>로그인된 채로 켜져</b> 있나요?<br>2) 지인 이름이 <b>카톡 친구 이름과 정확히 같나요?</b><br>3) 발송 중에는 <b>마우스·키보드를 절대 만지지 마세요</b> (약 15초/명)<br>4) 긴급 중단: 마우스를 <b>화면 왼쪽 위 모서리</b>로 밀기<br><span class="hint">처음엔 본인/가족 1명으로 테스트하세요.</span>
  </div>
  <div id="aRun" style="display:none;text-align:left">
    <div class="prog" id="aProg" style="font-size:16px;margin-bottom:6px"></div>
    <pre id="aLog" style="background:var(--cream);border-radius:8px;padding:10px;height:220px;overflow:auto;font-size:12px;margin:0;white-space:pre-wrap"></pre>
  </div>
  <div class="row" style="justify-content:center;margin-top:16px">
    <button class="primary" id="aGo" style="font-size:17px;padding:12px 26px">확인했습니다, 시작</button>
    <button id="aStop" style="display:none;color:var(--warn)">중단</button>
    <button class="ghost" id="aClose">닫기</button>
  </div>
</div></div>
<div class="modal" id="guideM"><div class="box" style="width:1040px;max-width:96vw;text-align:left">
  <div class="row between"><div class="who" style="font-size:22px;margin:0">사용법</div><button class="ghost" id="gClose">닫기</button></div>
  <div class="row" id="gTabs" style="margin:10px 0"></div>
  <img id="gImg" style="width:100%;border-radius:10px;display:block;background:var(--cream)">
  <p class="hint" style="margin:8px 0 0">장면이 약 2초마다 넘어갑니다. 다시 보려면 탭을 한 번 더 누르세요.</p>
</div></div>
<div class="modal" id="adminM"><div class="box" style="width:640px;text-align:left">
  <div class="row between"><div class="who" style="font-size:22px;margin:0">관리자</div><button class="ghost" id="admClose">닫기</button></div>
  <div id="admLogin" style="margin-top:12px">
    <p class="hint">관리자 비밀번호를 입력하세요.</p>
    <div class="row"><input id="admPw" type="password" placeholder="비밀번호 4자리" maxlength="4" inputmode="numeric" style="width:200px;letter-spacing:.3em;text-align:center;font-size:20px"><button class="primary" id="admLoginBtn">확인</button><span class="hint" id="admLoginMsg"></span></div>
  </div>
  <div id="admPanel" style="display:none;margin-top:12px">
    <div id="adminBox" style="border:2px solid var(--olive);border-radius:12px;padding:14px 16px;background:var(--sage)">
      <h2 style="margin:0 0 8px">프로그램 업데이트 올리기</h2>
      <div id="admNoKey" class="hint" style="display:none;color:var(--warn)">이 PC에는 업로드 열쇠(github_token.txt)가 없어 올리기를 할 수 없습니다. 개발자 PC에서만 가능합니다.</div>
      <div id="admUp">
        <p class="hint" style="margin:0 0 10px">올릴 파일을 고르세요 (보통 py 파일만: server.py · make_card.py · kakao_auto.py · ui.py / 구절·설정을 바꿨을 때만 verses.json · settings.json). 고르지 않은 파일은 서버의 기존 것이 유지됩니다.</p>
        <div class="row" style="margin-bottom:8px"><button id="admPick">📂 파일 선택…</button><input type="file" id="admFiles" multiple accept=".py,.json" style="display:none"><span class="hint" id="admPickMsg">선택된 파일 없음</span></div>
        <div id="admList" style="display:none;background:var(--paper);border-radius:8px;padding:8px 12px;margin-bottom:8px;font-size:14px;line-height:1.8"></div>
        <div class="row" style="margin-bottom:8px"><label style="width:70px;color:var(--gray)">서버 버전</label><span id="admCur" class="hint"></span></div>
        <div class="row" style="margin-bottom:8px"><label style="width:70px;color:var(--gray)">새 버전</label><input id="admVer" placeholder="예: 1.0.2" style="width:120px"><label style="color:var(--gray);margin-left:10px">바뀐 점</label><input id="admNotes" placeholder="예: 구절 추가" style="flex:1"></div>
        <div class="row"><button class="primary" id="admGo" disabled>업데이트 올리기</button><span class="hint" id="admMsg"></span></div>
        <pre id="admLog" style="display:none;background:var(--paper);border-radius:8px;padding:8px;font-size:12px;margin:8px 0 0;white-space:pre-wrap"></pre>
      </div>
    </div>
    <h2 style="margin:18px 0 8px">비밀번호 변경</h2>
    <div class="row"><input id="pwOld" type="password" placeholder="현재 비밀번호" style="width:150px"><input id="pwNew" type="password" placeholder="새 비밀번호 (4자리)" maxlength="4" style="width:150px"><input id="pwNew2" type="password" placeholder="새 비밀번호 확인" maxlength="4" style="width:150px"><button id="pwBtn">변경</button></div>
    <p class="hint" id="pwMsg"></p>
  </div>
</div></div>
<div class="toast" id="toast"></div>

<script>
let D={verses:{},contacts:[],history:[],next_day:1,windows:true};
let curTopic=null, curIdx=null, curFile=null, curDay=1;
const $=s=>document.querySelector(s);
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function toast(m){const t=$("#toast");t.textContent=m;t.classList.add("on");setTimeout(()=>t.classList.remove("on"),2200)}
async function api(p,b){const r=await fetch(p,b?{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(b)}:{});return r.json()}

async function load(){let ok=false;for(let i=0;i<6&&!ok;i++){try{D=await api("/api/data");if(D&&D.verses)ok=true;else throw new Error(D.error||"응답 오류")}catch(e){if(i<5){await new Promise(r=>setTimeout(r,1500));continue}document.body.insertAdjacentHTML("afterbegin",`<div style="background:#B7532F;color:#fff;padding:12px 20px;font-weight:700">데이터를 불러오지 못했습니다: ${e}<br>창을 닫고 20초 뒤 다시 실행해 보세요.</div>`);return}}
  if(D.license.settings.error)document.body.insertAdjacentHTML("afterbegin",`<div style="background:#F6E4DC;color:#B7532F;padding:10px 20px;font-weight:700">⚠ ${esc(D.license.settings.error)} — 기본값으로 실행 중입니다.</div>`);curDay=D.next_day;$("#day").value=curDay;renderTopics();renderContacts();renderPeople();renderHist();renderQueue();stat()}
function stat(){const L=D.license;const who=L.user?`${L.user}님 · `:"";const st=L.free_mode?"":(L.licensed?`이용권 ~${L.license_exp}`:(L.trial_left>0?`무료 ${L.trial_left}일 남음`:"무료 기간 종료"));$("#stat").textContent=`${who}${st?st+" · ":""}지인 ${D.contacts.length}명 · 발송 ${D.history.length}건`;
  $("#lock").style.display=L.active?"none":"block";$("#lock").innerHTML=`무료 이용 기간(${L.settings.trial_days}일)이 끝났습니다. 발송 이력은 계속 볼 수 있지만 새 카드는 만들 수 없습니다. → <a href="#" onclick="document.querySelector('nav button[data-p=set]').click();return false" style="color:inherit">설정·후원 탭에서 이용권 등록</a>`;
  $("#btnMake").disabled=!L.active;renderSettings();if(!L.user){$("#welcome").classList.add("on");$("#wTrial").textContent=L.free_mode?"기간 제한 없이 자유롭게 사용하실 수 있습니다.":`처음 ${L.settings.trial_days}일은 무료로 모든 기능을 쓸 수 있습니다.`;setTimeout(()=>$("#wName").focus(),100)}}
function renderSettings(){const L=D.license,S=L.settings;$("#sUser").value=L.user||"";$("#sFirst").textContent=L.first_run;
  $("#sStatus").innerHTML=L.free_mode?`<span class="tag">자유 이용</span> 기간 제한 없이 사용할 수 있습니다${L.licensed?` · <span class="tag">후원자 (광고 없음)</span> ${L.license_exp}까지`:""}`:L.licensed?`<span class="tag">이용권 등록됨</span> ${esc(L.license_name)} · ${L.license_exp}까지`:(L.trial_left>0?`<span class="tag">무료 체험</span> ${L.trial_left}일 남음`:`<span class="tag" style="background:#F6E4DC;color:#B7532F">무료 기간 종료</span>`);
  $("#sDonate").innerHTML=(L.free_mode?`<p style="margin:0 0 8px">이 프로그램은 <b>${esc(S.developer)}</b>이(가) 만들었습니다. <b>기간 제한 없이 무료로</b> 쓰실 수 있습니다.</p><p style="margin:0 0 12px;color:var(--gray);line-height:1.8">🙏 혹시 이 도구가 사역과 일상에 도움이 되셨다면, 원하시는 만큼 후원으로 응원해 주셔도 됩니다.<br>🌱 후원은 프로그램을 계속 다듬고 새 구절을 더하는 데 쓰입니다. 부담 갖지 않으셔도 됩니다. 😊</p>`:`<p style="margin:0 0 8px">이 프로그램은 <b>${esc(S.developer)}</b>이(가) 만들었습니다. 처음 ${S.trial_days}일은 무료이며, 이후에는 후원으로 이용권을 받아 계속 쓸 수 있습니다.</p>`)+`
    ${L.free_mode?"":`<div style="display:flex;gap:10px;margin:0 0 12px">
      <div class="plan" data-plan="month" style="flex:1;border-radius:10px;padding:12px 14px;cursor:pointer"><div class="hint">월 후원</div><div style="font-family:NM;font-weight:800;font-size:24px">${esc(S.price_month)}</div><div class="hint">1개월 이용권</div></div>
      <div class="plan" data-plan="year" style="flex:1;border-radius:10px;padding:12px 14px;cursor:pointer"><div class="hint">연 후원 · 추천</div><div style="font-family:NM;font-weight:800;font-size:24px">${esc(S.price_year)}</div><div class="hint">12개월 이용권</div></div>
    </div><p class="hint" id="planMsg" style="margin:0 0 8px"></p>`}
    ${S.price_text?`<p style="margin:0 0 8px" class="hint">${esc(S.price_text).replace(/\\n|\n/g,"<br>")}</p>`:""}
    ${S.donate_url?`<p style="margin:0 0 8px"><a href="${esc(S.donate_url)}" target="_blank" style="display:inline-block;background:#FEE500;color:#191919;font-weight:700;padding:10px 18px;border-radius:8px;text-decoration:none">💛 카카오페이로 후원하기</a></p>`:""}
    ${S.donate_account?`<p style="margin:0 0 8px"><b>후원 계좌:</b> ${esc(S.donate_account)} <button class="ghost" onclick="navigator.clipboard.writeText('${esc(S.donate_account)}').then(()=>toast('계좌가 복사되었습니다'))">계좌 복사</button></p>`:""}
    ${S.contact?`<p style="margin:0;color:var(--gray)">${L.free_mode?"문의·후원 연락처":"후원 후 연락"}: ${esc(S.contact)}${L.free_mode?" (후원 후 연락 주시면 광고 제거 코드를 보내드립니다)":" → 이용권 키를 보내드립니다"}</p>`:""}`;
  if(S.dedication){$("#dedication").innerHTML="🌿 "+esc(S.dedication);$("#dedication").style.display="block"}
  $("#sDonateTitle").textContent=L.free_mode?"만든 사람 · 후원":"이용권 · 후원";
  $("#sKeyRow").style.display="flex";$("#liLicense").style.display=L.free_mode?"none":"";$("#liFree").style.display=L.free_mode?"":"none";document.querySelectorAll(".plan .hint").forEach(x=>{if(L.free_mode&&x.textContent.includes("이용권"))x.textContent=x.textContent.replace("이용권","후원")});
  const pick=p=>{if(!$("#planMsg"))return;document.querySelectorAll(".plan").forEach(x=>x.classList.toggle("on",x.dataset.plan===p));$("#planMsg").textContent=L.free_mode?(p==="month"?`월 후원 — ${S.price_month}. 감사합니다.`:`연 후원 — ${S.price_year}. 감사합니다.`):(p==="month"?`선택: 월 후원 — ${S.price_month} 입금 후 연락주시면 1개월 이용권 키를 보내드립니다.`:`선택: 연 후원 — ${S.price_year} 입금 후 연락주시면 12개월 이용권 키를 보내드립니다.`)};
  document.querySelectorAll(".plan").forEach(x=>x.onclick=()=>pick(x.dataset.plan));pick(window._plan||"year");loadAds()}
async function loadAds(){try{const r=await api("/api/ads");const box=$("#adBox");if(!r.show||!r.ads.length){box.style.display="none";return}
  $("#adList").innerHTML=r.ads.map(a=>`<a href="${esc(a.link||"#")}" target="_blank" style="display:block;border:1px solid var(--line);border-radius:10px;overflow:hidden;text-decoration:none;color:var(--ink);background:var(--paper)">${a.img?`<img src="${esc(a.img)}" style="width:100%;display:block">`:""}${a.text?`<div style="padding:10px 12px;font-size:14px">${esc(a.text)}</div>`:""}</a>`).join("");box.style.display="block"}catch(e){}}
$("#wGo").onclick=async()=>{const n=$("#wName").value.trim();if(!n)return toast("이름을 입력하세요");const r=await api("/api/profile",{user:n});D.license=r.license;$("#welcome").classList.remove("on");stat();toast(n+"님, 환영합니다")};
$("#wName").addEventListener("keydown",e=>{if(e.key==="Enter")$("#wGo").click()});
$("#sLog").onclick=async()=>{const r=await fetch("/api/startlog");$("#sLogBox").textContent=await r.text();$("#sLogBox").style.display="block"};
$("#bkDown").onclick=async()=>{const r=await api("/api/backup",{});const blob=new Blob([JSON.stringify(r.data,null,1)],{type:"application/json"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=`말씀배달부_백업_${new Date().toISOString().slice(0,10)}.json`;a.click();toast("백업 파일을 저장했습니다")};
$("#bkUpBtn").onclick=()=>$("#bkUp").click();
$("#bkUp").onchange=async e=>{const f=e.target.files[0];if(!f)return;if(!confirm("현재 지인·이력이 백업 파일 내용으로 교체됩니다. 계속할까요?"))return;const d=JSON.parse(await f.text());const r=await api("/api/restore",{data:d});if(!r.ok)return toast(r.error);toast("복원 완료");setTimeout(()=>location.reload(),800)};
$("#sBg").onclick=()=>api("/api/open_bg",{});$("#sOut").onclick=()=>api("/api/open_output",{});
$("#sUserSave").onclick=async()=>{const r=await api("/api/profile",{user:$("#sUser").value});D.license=r.license;stat();toast("저장됨")};
$("#sKeyBtn").onclick=async()=>{const r=await api("/api/activate",{key:$("#sKey").value});if(!r.ok){$("#sKeyMsg").textContent=r.error;return}D.license=r.license;$("#sKey").value="";$("#sKeyMsg").textContent="등록되었습니다. 감사합니다!";stat();toast("후원자 코드 등록 완료")};

/* 주제/구절 */
function renderTopics(){const t=$("#topics");t.innerHTML="";Object.keys(D.verses).forEach(k=>{const b=document.createElement("button");b.innerHTML=`${esc(k)}<span class="n">${D.verses[k].length}</span>`;b.className=k===curTopic?"on":"";b.onclick=()=>{curTopic=k;curIdx=null;renderTopics();renderVerses()};t.appendChild(b)});
  const s=$("#fTopic");if(s.options.length<=1)Object.keys(D.verses).forEach(k=>s.add(new Option(k,k)))}
function sentTo(ref){const m={};D.history.filter(h=>h.ref===ref).forEach(h=>m[h.name]=1);return Object.keys(m)}
function renderVerses(){const box=$("#verses");box.innerHTML="";$("#topicTitle").textContent=curTopic?`${curTopic} — ${D.verses[curTopic].length}구절`:"주제를 고르세요";if(!curTopic)return;
  D.verses[curTopic].forEach((v,i)=>{const s=sentTo(v.ref);const d=document.createElement("div");d.className="verse"+(i===curIdx?" on":"");
    d.innerHTML=`<span class="ref">${esc(v.ref)} · ${esc(v.book)}${v.mine?' <span class="tag">내가 추가</span>':""}</span><span class="sent">${s.length?`<b>${s.length}명</b>에게 보냄`:"아직 안 보냄"}${v.mine?` <button class="del" data-id="${v.id}" style="border:none;padding:2px 6px;color:var(--gray)">삭제</button>`:""}</span><div class="txt">${esc(v.text)}</div><div class="decl">${esc(v.declaration).replace(/\n/g,"<br>")}</div>`;
    if(v.mine)d.querySelector(".del").onclick=async e=>{e.stopPropagation();if(!confirm("이 구절을 삭제할까요?"))return;const r=await api("/api/myverse_delete",{id:v.id});D.verses=r.verses;curIdx=null;$("#make").style.display="none";renderTopics();renderVerses();renderQueue()};
    d.onclick=()=>{curIdx=i;renderVerses();$("#make").style.display="flex";$("#selRef").textContent="선택: "+v.ref;$("#makeMsg").textContent=""};box.appendChild(d)})}

/* 구절 직접 추가 */
$("#aLook").onclick=async()=>{const r=await api("/api/lookup",{ref:$("#aRef").value});$("#aMsg").textContent=r.ok?r.book:r.error;$("#aText").textContent=r.text||""};
$("#aRef").addEventListener("keydown",e=>{if(e.key==="Enter")$("#aLook").click()});
$("#aAdd").onclick=async()=>{if(!curTopic)return toast("먼저 왼쪽에서 주제를 고르세요");if(!$("#aDecl").value.trim())return toast("선포문을 입력하세요");
  const r=await api("/api/myverse_add",{topic:curTopic,ref:$("#aRef").value,declaration:$("#aDecl").value});if(!r.ok)return toast(r.error);
  D.verses=r.verses;$("#aRef").value="";$("#aDecl").value="";$("#aText").textContent="";$("#aMsg").textContent="";renderTopics();renderVerses();renderQueue();toast("구절이 추가되었습니다")};

/* 카드 만들기 */
$("#btnMake").onclick=async()=>{if(curTopic==null||curIdx==null)return;const day=parseInt($("#day").value)||1;$("#btnMake").disabled=true;$("#makeMsg").textContent="만드는 중… (10초쯤 걸려요)";
  const r=await api("/api/card",{topic:curTopic,idx:curIdx,day});$("#btnMake").disabled=false;
  if(!r.ok){$("#makeMsg").textContent="실패: "+r.error;return}
  curFile=r.file;curDay=day;$("#makeMsg").textContent="완성! 배경: "+r.bg;$("#cardImg").innerHTML=`<img src="/output/${encodeURIComponent(r.file)}?t=${Date.now()}">`;$("#sendBox").style.display="block";renderContacts()};
$("#btnFolder").onclick=()=>api("/api/open_output",{});

/* 받을 사람 */
function curRef(){return D.verses[curTopic][curIdx].ref}
function renderContacts(){const c=$("#cList");c.innerHTML="";if(!D.contacts.length){c.innerHTML='<div class="hint" style="padding:8px">지인 관리 탭에서 먼저 사람을 추가하세요.</div>';return}
  const already=curTopic!=null&&curIdx!=null?sentTo(curRef()):[];const q=($("#cFind").value||"").trim();
  D.contacts.forEach((p,i)=>{if(q&&!(p.name.includes(q)||(p.memo||"").includes(q)||(p.group||"").includes(q)))return;const dup=already.includes(p.name);const l=document.createElement("label");l.className=dup?"dup":"";
    l.innerHTML=`<input type="checkbox" data-i="${i}"><span>${esc(p.name)}</span>${dup?'<span class="tag" style="background:#F6E4DC;color:#B7532F">이 구절 이미 받음</span>':""}<span class="g">${esc(p.group)}${p.memo?" · "+esc(p.memo):""}</span>`;c.appendChild(l)})}
function checked(){return [...document.querySelectorAll("#cList input:checked")].map(x=>D.contacts[+x.dataset.i])}
$("#cFind").addEventListener("input",()=>{const keep=new Set([...document.querySelectorAll("#cList input:checked")].map(x=>x.dataset.i));renderContacts();document.querySelectorAll("#cList input").forEach(x=>{if(keep.has(x.dataset.i))x.checked=true})});
document.addEventListener("keydown",e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==="f"){const t=document.querySelector(".page.on").id;if(t==="p-make"&&$("#sendBox").style.display!=="none"){e.preventDefault();$("#cFind").focus();$("#cFind").select()}else if(t==="p-hist"){e.preventDefault();$("#fName").focus()}else if(t==="p-custom"){e.preventDefault();$("#qFind").focus()}}});
$("#selAll").onclick=()=>document.querySelectorAll("#cList input").forEach(x=>x.checked=true);
$("#selNone").onclick=()=>document.querySelectorAll("#cList input").forEach(x=>x.checked=false);

async function copyCard(){if(!curFile)return false;const r=await api("/api/copy",{file:curFile});if(!r.ok){toast("복사 실패: "+(r.error||"윈도우에서만 됩니다"));return false}return true}
$("#btnCopy").onclick=async()=>{if(await copyCard())toast("카드 복사됨 — 카톡에서 Ctrl+V")};

async function record(list,job){if(!list.length)return;const j=job||{topic:curTopic,ref:D.verses[curTopic][curIdx].ref,day:curDay,file:curFile};
  const r=await api("/api/history",{entries:list.map(p=>({name:p.name,group:p.group,topic:j.topic,ref:j.ref,day:j.day,file:j.file}))});
  D.history=r.history;D.next_day=Math.max(D.next_day,j.day+1);if(curTopic)renderVerses();renderContacts();renderPeople();renderHist();renderQueue();stat()}
$("#btnMark").onclick=async()=>{const l=checked();if(!l.length)return toast("받을 사람을 체크하세요");await record(l);toast(`${l.length}명 기록 완료`);$("#selNone").click()};

/* 한 명씩 보내기 */
let queue=[],qi=0;   // queue 항목: {p:지인, job:{topic,idx,ref,day,file}}  job.file 없으면 그때 카드 생성
$("#btnStep").onclick=async()=>{const l=checked();if(!l.length)return toast("받을 사람을 체크하세요");
  queue=l.map(p=>({p,job:{topic:curTopic,idx:curIdx,ref:curRef(),day:curDay,file:curFile}}));qi=0;$("#modal").classList.add("on");await showStep()};
async function showStep(){if(qi>=queue.length){$("#modal").classList.remove("on");toast("모두 완료!");$("#selNone").click();return}
  const q=queue[qi];$("#mProg").textContent=`${qi+1} / ${queue.length}`;$("#mWho").textContent=q.p.name;$("#mInfo").textContent=`${q.job.topic} · ${q.job.ref} · ${q.job.day}일차`;$("#mImg").style.display="none";
  if(!q.job.file){$("#mSteps").innerHTML="카드 만드는 중… (10초쯤)";$("#mDone").disabled=true;const r=await api("/api/card",{topic:q.job.topic,idx:q.job.idx,day:q.job.day});$("#mDone").disabled=false;
    if(!r.ok){$("#mSteps").innerHTML="카드 생성 실패: "+esc(r.error);return}q.job.file=r.file}
  curFile=q.job.file;$("#mImg").src=`/output/${encodeURIComponent(q.job.file)}?t=${Date.now()}`;$("#mImg").style.display="block";
  $("#mSteps").innerHTML="카드가 복사되었습니다.<br>카톡에서 <b>이 사람 대화방</b>을 열고 <b>Ctrl+V</b> 후 <b>Enter</b>로 전송하세요.";await copyCard()}
$("#mDone").onclick=async()=>{const q=queue[qi];await record([q.p],q.job);qi++;await showStep()};
$("#mSkip").onclick=async()=>{qi++;await showStep()};
$("#mRecopy").onclick=async()=>{if(await copyCard())toast("다시 복사됨")};

/* 카톡 자동 발송 */
let autoJobs=[],autoTimer=null;
function openAuto(jobs){if(!jobs.length)return toast("보낼 사람을 체크하세요");autoJobs=jobs;$("#aWarn").style.display="block";$("#aRun").style.display="none";$("#aGo").style.display="inline-block";$("#aStop").style.display="none";$("#aGo").disabled=false;$("#autoM").classList.add("on")}
$("#aGo").onclick=async()=>{$("#aGo").disabled=true;$("#aWarn").style.display="none";$("#aRun").style.display="block";$("#aLog").textContent="카드 준비 중… (사람 수 × 10초)";
  const r=await api("/api/auto_start",{jobs:autoJobs});if(!r.ok){$("#aLog").textContent=r.error;return}
  $("#aGo").style.display="none";$("#aStop").style.display="inline-block";let recorded=0;
  autoTimer=setInterval(async()=>{const s=await api("/api/auto_status");$("#aProg").textContent=s.running?`${s.index} / ${s.total} — ${s.current} 보내는 중…`:`완료: 성공 ${s.done.length}명, 실패 ${s.failed.length}명`;
    $("#aLog").textContent=s.log.join("\n");$("#aLog").scrollTop=99999;
    if(!s.running){clearInterval(autoTimer);$("#aStop").style.display="none";
      for(const d of s.done.slice(recorded)){const m=d.meta;const p=D.contacts.find(c=>c.name===m.name)||{name:m.name,group:""};await record([p],{topic:m.topic,ref:m.ref,day:m.day,file:m.file})}recorded=s.done.length}},1500)};
$("#aStop").onclick=()=>api("/api/auto_stop",{});
$("#aClose").onclick=()=>{$("#autoM").classList.remove("on");if(autoTimer)clearInterval(autoTimer)};
$("#btnAuto").onclick=()=>{const l=checked();if(!l.length)return toast("받을 사람을 체크하세요");if(!curFile)return toast("먼저 카드를 만드세요");
  openAuto(l.map(p=>({name:p.name,topic:curTopic,idx:curIdx,ref:curRef(),day:curDay,file:curFile})))};
$("#qAuto").onclick=()=>{const names=[...document.querySelectorAll(".qchk:checked")].map(x=>x.dataset.n);if(!names.length)return toast("보낼 사람을 체크하세요");
  const missing=names.filter(n=>!plan[n].topic);if(missing.length)return toast(`주제를 안 고른 사람: ${missing.join(", ")}`);
  openAuto(names.map(n=>{const pl=plan[n];return{name:n,topic:pl.topic,idx:pl.idx,ref:D.verses[pl.topic][pl.idx].ref,day:pl.day,file:null}}))};

/* 맞춤 발송 */
let plan={};  // name -> {topic, idx, day}
function renderQueue(){const t=$("#qTable");t.innerHTML="";const topics=Object.keys(D.verses);
  const q=($("#qFind").value||"").trim();
  D.contacts.forEach(p=>{const pl=plan[p.name]||(plan[p.name]={topic:"",idx:0,day:D.next_day});if(q&&!(p.name.includes(q)||(p.memo||"").includes(q)))return;const tr=document.createElement("tr");
    const sent=pl.topic?sentTo(D.verses[pl.topic][pl.idx].ref).includes(p.name):false;
    tr.innerHTML=`<td><input type="checkbox" class="qchk" data-n="${esc(p.name)}" ${pl.topic?"checked":""}></td><td><b>${esc(p.name)}</b></td><td class="hint">${esc(p.memo||"")}</td>
      <td><select class="qsel qt" data-n="${esc(p.name)}"><option value="">- 주제 -</option>${topics.map(k=>`<option ${k===pl.topic?"selected":""}>${esc(k)}</option>`).join("")}</select></td>
      <td><select class="qsel qv" data-n="${esc(p.name)}" ${pl.topic?"":"disabled"}>${pl.topic?D.verses[pl.topic].map((v,i)=>`<option value="${i}" ${i===pl.idx?"selected":""}>${esc(v.ref)} ${esc(v.text.slice(0,18))}…</option>`).join(""):""}</select></td>
      <td><input type="number" class="qsel qd" data-n="${esc(p.name)}" value="${pl.day}" min="1" style="width:70px;text-align:center"></td>
      <td>${sent?'<span class="tag" style="background:#F6E4DC;color:#B7532F">이미 받음</span>':""}</td>`;t.appendChild(tr)});
  t.querySelectorAll(".qt").forEach(s=>s.onchange=()=>{plan[s.dataset.n].topic=s.value;plan[s.dataset.n].idx=0;renderQueue()});
  t.querySelectorAll(".qv").forEach(s=>s.onchange=()=>{plan[s.dataset.n].idx=+s.value;renderQueue()});
  t.querySelectorAll(".qd").forEach(s=>s.onchange=()=>{plan[s.dataset.n].day=parseInt(s.value)||1})}
$("#qFind").addEventListener("input",renderQueue);
$("#qAll").onchange=()=>document.querySelectorAll(".qchk").forEach(x=>x.checked=$("#qAll").checked);
$("#qSame").onclick=()=>{const first=D.contacts.map(p=>plan[p.name]).find(x=>x&&x.topic);if(!first)return toast("첫 번째 줄에서 주제와 구절을 먼저 고르세요");
  document.querySelectorAll(".qchk:checked").forEach(x=>{plan[x.dataset.n]={topic:first.topic,idx:first.idx,day:first.day}});renderQueue();toast("같은 말씀으로 채웠습니다")};
$("#qClear").onclick=()=>{plan={};renderQueue()};
$("#qStart").onclick=async()=>{const names=[...document.querySelectorAll(".qchk:checked")].map(x=>x.dataset.n);if(!names.length)return toast("보낼 사람을 체크하세요");
  const missing=names.filter(n=>!plan[n].topic);if(missing.length)return toast(`주제를 안 고른 사람: ${missing.join(", ")}`);
  queue=names.map(n=>{const p=D.contacts.find(c=>c.name===n),pl=plan[n];return{p,job:{topic:pl.topic,idx:pl.idx,ref:D.verses[pl.topic][pl.idx].ref,day:pl.day,file:null}}});
  qi=0;$("#modal").classList.add("on");await showStep()};
$("#mStop").onclick=()=>$("#modal").classList.remove("on");

/* 지인 관리 */
function renderPeople(){const t=$("#cTable");t.innerHTML="";$("#cCount").textContent=D.contacts.length+"명";
  D.contacts.forEach((p,i)=>{const hs=D.history.filter(h=>h.name===p.name);const last=hs.length?hs[hs.length-1].sent_at.slice(0,10):"-";
    const tr=document.createElement("tr");tr.innerHTML=`<td><b>${esc(p.name)}</b></td><td>${esc(p.group)}</td><td>${esc(p.memo||"")}</td><td>${hs.length}장</td><td>${last}</td><td><button class="del" data-i="${i}">삭제</button></td>`;t.appendChild(tr)});
  t.querySelectorAll(".del").forEach(b=>b.onclick=async()=>{const p=D.contacts[+b.dataset.i];if(!confirm(`${p.name} 님을 목록에서 지울까요? (발송 이력은 남습니다)`))return;D.contacts.splice(+b.dataset.i,1);await api("/api/contacts",{contacts:D.contacts});renderPeople();renderContacts();renderQueue();stat()})}
$("#btnAdd").onclick=async()=>{const name=$("#cName").value.trim();if(!name)return toast("이름을 입력하세요");if(D.contacts.some(c=>c.name===name))return toast("이미 있는 이름입니다");
  D.contacts.push({name,group:$("#cGroup").value,memo:$("#cMemo").value.trim()});await api("/api/contacts",{contacts:D.contacts});$("#cName").value="";$("#cMemo").value="";renderPeople();renderContacts();renderQueue();stat();toast(name+" 추가됨")};
$("#cName").addEventListener("keydown",e=>{if(e.key==="Enter")$("#btnAdd").click()});
$("#cMemo").addEventListener("keydown",e=>{if(e.key==="Enter")$("#btnAdd").click()});

/* 발송 이력 */
function renderHist(){const t=$("#hTable");t.innerHTML="";const n=$("#fName").value.trim(),tp=$("#fTopic").value,rf=$("#fRef").value.trim();
  const rows=[...D.history].reverse().filter(h=>(!n||h.name.includes(n))&&(!tp||h.topic===tp)&&(!rf||h.ref.includes(rf)));
  $("#hCount").textContent=rows.length+"건";
  rows.forEach(h=>{const tr=document.createElement("tr");tr.innerHTML=`<td>${esc(h.sent_at)}</td><td><b>${esc(h.name)}</b></td><td>${h.day}일차</td><td><span class="tag">${esc(h.topic)}</span></td><td>${esc(h.ref)}</td><td><a href="/output/${encodeURIComponent(h.file||"")}" target="_blank" style="color:var(--olive)">보기</a></td><td><button class="del" data-id="${h.id}">삭제</button></td>`;t.appendChild(tr)});
  t.querySelectorAll(".del").forEach(b=>b.onclick=async()=>{if(!confirm("이 기록을 지울까요?"))return;const r=await api("/api/history_delete",{id:b.dataset.id});D.history=r.history;renderHist();renderPeople();renderVerses();renderContacts();stat()})}
["#fName","#fRef"].forEach(s=>$(s).addEventListener("input",renderHist));$("#fTopic").addEventListener("change",renderHist);
$("#fClear").onclick=()=>{$("#fName").value="";$("#fRef").value="";$("#fTopic").value="";renderHist()};

/* 사용법 */
const GUIDES=[["전체","전체.gif"],["시작","시작.gif"],["지인 관리","지인관리.gif"],["카드 만들기","카드만들기.gif"],["맞춤 발송","맞춤발송.gif"],["발송 이력","발송이력.gif"],["설정","설정.gif"]];
function openGuide(name){$("#guideM").classList.add("on");$("#gTabs").innerHTML=GUIDES.map(g=>`<button class="${g[0]===name?"primary":""}" data-g="${g[1]}" data-n="${g[0]}">${g[0]}</button>`).join("");
  document.querySelectorAll("#gTabs button").forEach(b=>b.onclick=()=>openGuide(b.dataset.n));const f=GUIDES.find(g=>g[0]===name)[1];$("#gImg").src=`/guide/${encodeURIComponent(f)}?t=${Date.now()}`}
$("#btnGuide").onclick=()=>openGuide("전체");$("#btnGuide2").onclick=()=>openGuide("전체");$("#gClose").onclick=()=>$("#guideM").classList.remove("on");

/* 탭 */
document.querySelectorAll("nav button").forEach(b=>b.onclick=()=>{document.querySelectorAll("nav button").forEach(x=>x.classList.toggle("on",x===b));document.querySelectorAll(".page").forEach(p=>p.classList.toggle("on",p.id==="p-"+b.dataset.p))});
setInterval(()=>fetch("/api/ping").catch(()=>{}),3000);
async function checkUpd(show){const u=await api("/api/update");$("#sDiag").textContent=u.diag||"";$("#sVer").textContent=(u.code_version?`코드 v${u.code_version}`:`v${u.app_version}`)+(u.source?` · ${u.source}`:"")+(u.code_notes?` — ${u.code_notes}`:"");if(show)toast("프로그램을 다시 실행하면 최신 코드가 자동 적용됩니다")}
setTimeout(()=>checkUpd(false),500);
let ADM_PW="";
async function loadAdmin(){const a=await api("/api/admin");$("#admNoKey").style.display=a.can_upload?"none":"block";$("#admUp").style.display=a.can_upload?"block":"none";
  $("#admCur").textContent=a.server.version?`v${a.server.version} (${(a.server.updated_at||"").slice(0,16)}) ${a.server.notes||""}`:"(아직 없음)";const v=(a.server.version||"1.0.0").split(".").map(Number);v[2]=(v[2]||0)+1;$("#admVer").value=v.join(".")}
$("#btnAdmin").onclick=()=>{$("#adminM").classList.add("on");if(ADM_PW){$("#admLogin").style.display="none";$("#admPanel").style.display="block";loadAdmin()}else{$("#admLogin").style.display="block";$("#admPanel").style.display="none";$("#admPw").value="";setTimeout(()=>$("#admPw").focus(),100)}};
$("#admClose").onclick=()=>$("#adminM").classList.remove("on");
$("#admLoginBtn").onclick=async()=>{const r=await api("/api/admin_login",{pw:$("#admPw").value});if(!r.ok){$("#admLoginMsg").textContent="비밀번호가 틀립니다";$("#admPw").value="";$("#admPw").focus();return}ADM_PW=$("#admPw").value;$("#admLoginMsg").textContent="";$("#admLogin").style.display="none";$("#admPanel").style.display="block";loadAdmin()};
$("#admPw").addEventListener("keydown",e=>{if(e.key==="Enter")$("#admLoginBtn").click()});
$("#admPw").addEventListener("input",()=>{$("#admLoginMsg").textContent="";if($("#admPw").value.length>=4)$("#admLoginBtn").click()});
const ADM_OK=["server.py","make_card.py","kakao_auto.py","ui.py","verses.json","settings.json"];let admSel=[];
$("#admPick").onclick=()=>$("#admFiles").click();
$("#admFiles").onchange=async e=>{admSel=[];const rows=[];for(const f of e.target.files){const ok=ADM_OK.includes(f.name);const buf=await f.arrayBuffer();let bin="";const u=new Uint8Array(buf);for(let i=0;i<u.length;i+=8192)bin+=String.fromCharCode.apply(null,u.subarray(i,i+8192));
    if(ok)admSel.push({name:f.name,data_b64:btoa(bin)});rows.push(`${ok?"✅":"⚠️"} ${esc(f.name)} <span class="hint">(${(f.size/1024).toFixed(1)} KB${ok?"":" — 대상 파일 아님, 건너뜀"})</span>`)}
  $("#admList").innerHTML=rows.join("<br>");$("#admList").style.display=rows.length?"block":"none";$("#admPickMsg").textContent=admSel.length?`${admSel.length}개 선택됨`:"선택된 파일 없음";$("#admGo").disabled=!admSel.length;e.target.value=""};
$("#admGo").onclick=async()=>{const ver=$("#admVer").value.trim();if(!/^\d+\.\d+\.\d+$/.test(ver))return toast("버전은 1.0.2 형식으로");if(!admSel.length)return toast("파일을 먼저 선택하세요");
  if(!confirm(`버전 ${ver} 으로 ${admSel.map(x=>x.name).join(", ")} 을 서버에 올립니다. 모든 사용자에게 적용됩니다. 진행할까요?`))return;
  $("#admGo").disabled=true;$("#admMsg").textContent="올리는 중…";const r=await api("/api/admin_upload_files",{pw:ADM_PW,files:admSel,version:ver,notes:$("#admNotes").value});$("#admGo").disabled=false;
  if(!r.ok){$("#admMsg").textContent=r.error;return}$("#admMsg").textContent=`완료! v${r.version} 배포됨`;$("#admLog").textContent=r.log.join("\n");$("#admLog").style.display="block";admSel=[];$("#admList").style.display="none";$("#admPickMsg").textContent="선택된 파일 없음";
  if(confirm(`v${r.version} 이 서버에 올라갔습니다. 프로그램을 다시 시작해서 바로 적용할까요?`)){document.body.insertAdjacentHTML("beforeend",`<div id="deadOv" style="position:fixed;inset:0;background:rgba(43,41,36,.7);color:#fff;display:flex;align-items:center;justify-content:center;font-size:18px;z-index:99">업데이트 적용 중… 잠시 후 자동으로 새로고침됩니다.</div>`);api("/api/restart",{}).catch(()=>{});setTimeout(()=>{const t=setInterval(async()=>{try{const r=await fetch("/api/ping");if(r.ok){clearInterval(t);location.reload()}}catch(e){}},400)},700)}else loadAdmin()};
$("#pwBtn").onclick=async()=>{if($("#pwNew").value.length!==4)return $("#pwMsg").textContent="새 비밀번호는 4자리";if($("#pwNew").value!==$("#pwNew2").value)return $("#pwMsg").textContent="새 비밀번호가 서로 다릅니다";const r=await api("/api/admin_setpw",{old:$("#pwOld").value,new:$("#pwNew").value});$("#pwMsg").textContent=r.ok?"변경되었습니다":r.error;if(r.ok){ADM_PW=$("#pwNew").value;$("#pwOld").value=$("#pwNew").value=$("#pwNew2").value=""}};fetch("/api/ping").catch(()=>{});
$("#btnQuit").onclick=async()=>{if(!confirm("프로그램을 종료할까요?"))return;await api("/api/quit",{});document.body.innerHTML='<div style="padding:60px;text-align:center;font-size:18px;color:#8B867C">종료되었습니다. 이 창을 닫으세요.</div>';setTimeout(()=>window.close(),800)};
load();
</script>
</body>
</html>
"""
