"""
TOEIC Pro 750+ — Streamlit 版
根據多益學習平台開發紀錄重建，獨立部署，不影響原 Netlify 網站。
"""
import random
import time
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TOEIC Pro 750+",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
:root {
  --pr: #2563eb; --gr: #10b981; --yl: #f59e0b;
  --rd: #ef4444; --bg: #f1f5f9; --tx: #1e293b; --mu: #64748b;
}
/* 隱藏 Streamlit 預設選單 */
#MainMenu, footer, header { visibility: hidden; }
.stTabs [data-baseweb="tab-list"] { gap: 4px; flex-wrap: wrap; }
.stTabs [data-baseweb="tab"] {
  border-radius: 8px 8px 0 0;
  padding: 8px 18px;
  font-weight: 600;
}
/* 卡片 */
.tcard {
  background: white; border-radius: 14px;
  padding: 1.4rem 1.6rem; margin-bottom: 1rem;
  box-shadow: 0 1px 3px rgba(0,0,0,.08);
  border: 1px solid #e2e8f0;
}
/* 儀表板數字 */
.stat-grid { display:flex; gap:12px; flex-wrap:wrap; margin-bottom:1rem; }
.stat-box {
  background:white; border-radius:12px; padding:1rem 1.4rem;
  border:1px solid #e2e8f0; flex:1; min-width:120px; text-align:center;
  box-shadow:0 1px 3px rgba(0,0,0,.06);
}
.stat-num { font-size:2rem; font-weight:800; color:var(--pr); line-height:1; }
.stat-lbl { font-size:.75rem; color:var(--mu); margin-top:4px; }
/* 單字翻牌 */
.flashcard {
  background:linear-gradient(135deg,#2563eb,#1d4ed8);
  color:white; border-radius:18px;
  padding:2.5rem 2rem; text-align:center;
  min-height:180px; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  cursor:pointer; margin-bottom:1rem;
  box-shadow: 0 8px 24px rgba(37,99,235,.25);
}
.fc-word { font-size:2.2rem; font-weight:800; letter-spacing:.04em; }
.fc-pos  { font-size:.85rem; opacity:.75; margin-top:.3rem; }
.fc-zh   { font-size:1.5rem; font-weight:700; margin-bottom:.5rem; }
.fc-ex   { font-size:.85rem; opacity:.85; line-height:1.5; }
/* 選項按鈕 */
.opt-btn {
  width:100%; background:white; border:2px solid #e2e8f0;
  border-radius:10px; padding:.7rem 1rem;
  text-align:left; cursor:pointer; font-size:.92rem;
  margin-bottom:.5rem; transition:all .15s; color:var(--tx);
}
.opt-btn:hover { border-color:var(--pr); }
.opt-correct { border-color:#10b981!important; background:#ecfdf5!important; }
.opt-wrong   { border-color:#ef4444!important; background:#fef2f2!important; }
/* 進度條 */
.pb-wrap { background:#e2e8f0; border-radius:99px; height:8px; overflow:hidden; margin:.5rem 0; }
.pb { height:100%; border-radius:99px; background:linear-gradient(90deg,#2563eb,#7c3aed); transition:width .4s; }
/* 回饋框 */
.fb-ok  { background:#ecfdf5; border:1px solid #10b981; border-radius:10px; padding:.8rem 1rem; color:#065f46; margin-top:.5rem; }
.fb-bad { background:#fef2f2; border:1px solid #ef4444; border-radius:10px; padding:.8rem 1rem; color:#991b1b; margin-top:.5rem; }
/* 標籤 */
.tag { display:inline-block; padding:.15rem .55rem; border-radius:6px; font-size:.72rem; font-weight:700; margin-right:.3rem; }
.tag-n   { background:#dbeafe; color:#1e40af; }
.tag-v   { background:#dcfce7; color:#166534; }
.tag-adj { background:#fef9c3; color:#854d0e; }
.tag-adv { background:#f3e8ff; color:#6b21a8; }
/* 計時器 */
.timer-box {
  text-align:center; font-size:2rem; font-weight:800;
  color:var(--pr); margin-bottom:.5rem;
}
.timer-warn   { color:var(--yl)!important; }
.timer-danger { color:var(--rd)!important; animation: blink 1s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.5} }
/* 英雄區塊 */
.hero {
  background:linear-gradient(135deg,#2563eb,#7c3aed);
  color:white; border-radius:16px; padding:1.8rem 2rem; margin-bottom:1.5rem;
}
.hero h1 { color:white; margin:0; font-size:1.8rem; font-weight:800; }
.hero p  { color:rgba(255,255,255,.85); margin:.3rem 0 0; }
/* 單字庫 */
.wl-row {
  display:flex; align-items:center; gap:.8rem;
  padding:.6rem .8rem; border-radius:8px;
  border-bottom:1px solid #f1f5f9;
}
.wl-word { font-weight:700; min-width:130px; }
.wl-zh   { color:var(--mu); flex:1; }
.wl-ex   { font-size:.78rem; color:#94a3b8; flex:2; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 資料層
# ─────────────────────────────────────────────────────────────────────────────
VOCAB = [
    # 商務辦公
    {"word":"accomplish","pos":"v.","cat":"商務辦公","zh":"完成、實現","ex":"She managed to accomplish the task ahead of schedule."},
    {"word":"acquire","pos":"v.","cat":"商務辦公","zh":"取得、獲得","ex":"The company plans to acquire new assets this year."},
    {"word":"allocate","pos":"v.","cat":"商務辦公","zh":"分配、撥出","ex":"The manager will allocate resources to each team."},
    {"word":"anticipate","pos":"v.","cat":"商務辦公","zh":"預期、預料","ex":"We anticipate strong sales growth in Q4."},
    {"word":"assemble","pos":"v.","cat":"商務辦公","zh":"集合、組裝","ex":"All staff are asked to assemble in the conference room."},
    {"word":"authorize","pos":"v.","cat":"商務辦公","zh":"授權、批准","ex":"Only the CEO can authorize this expenditure."},
    {"word":"collaborate","pos":"v.","cat":"商務辦公","zh":"合作","ex":"Both departments need to collaborate on this project."},
    {"word":"compensate","pos":"v.","cat":"商務辦公","zh":"補償","ex":"The firm will compensate employees for overtime."},
    {"word":"comprehensive","pos":"adj.","cat":"商務辦公","zh":"全面的、完整的","ex":"Please submit a comprehensive report by Friday."},
    {"word":"consistently","pos":"adv.","cat":"商務辦公","zh":"一致地、持續地","ex":"She consistently delivers high-quality work."},
    {"word":"deadline","pos":"n.","cat":"商務辦公","zh":"截止日期","ex":"We must meet the deadline by noon tomorrow."},
    {"word":"delegate","pos":"v.","cat":"商務辦公","zh":"委派、授權","ex":"A good manager knows when to delegate tasks."},
    {"word":"demonstrate","pos":"v.","cat":"商務辦公","zh":"展示、證明","ex":"Please demonstrate how the software works."},
    {"word":"efficient","pos":"adj.","cat":"商務辦公","zh":"有效率的","ex":"An efficient process saves both time and money."},
    {"word":"eliminate","pos":"v.","cat":"商務辦公","zh":"消除、排除","ex":"We need to eliminate unnecessary steps in the workflow."},
    {"word":"evaluate","pos":"v.","cat":"商務辦公","zh":"評估、評價","ex":"The committee will evaluate the proposals next week."},
    {"word":"facilitate","pos":"v.","cat":"商務辦公","zh":"促進、協助","ex":"Technology can facilitate remote collaboration."},
    {"word":"implement","pos":"v.","cat":"商務辦公","zh":"實施、執行","ex":"The team will implement the new system next month."},
    {"word":"mandatory","pos":"adj.","cat":"商務辦公","zh":"強制的、必須的","ex":"Attendance at the safety training is mandatory."},
    {"word":"negotiate","pos":"v.","cat":"商務辦公","zh":"談判、協商","ex":"Both sides need to negotiate a fair contract."},
    {"word":"prioritize","pos":"v.","cat":"商務辦公","zh":"優先處理","ex":"Please prioritize the client requests this week."},
    {"word":"proposal","pos":"n.","cat":"商務辦公","zh":"提案、建議書","ex":"Please review the proposal before the meeting."},
    {"word":"qualified","pos":"adj.","cat":"商務辦公","zh":"有資格的","ex":"Only qualified applicants will be interviewed."},
    {"word":"reliable","pos":"adj.","cat":"商務辦公","zh":"可靠的","ex":"We need a reliable supplier for our materials."},
    {"word":"schedule","pos":"v.","cat":"商務辦公","zh":"排定、安排","ex":"Please schedule the meeting for next Tuesday."},
    # 財務會計
    {"word":"accountable","pos":"adj.","cat":"財務會計","zh":"負責任的","ex":"Each manager is accountable for their department's budget."},
    {"word":"annual","pos":"adj.","cat":"財務會計","zh":"年度的","ex":"The annual report will be released next month."},
    {"word":"asset","pos":"n.","cat":"財務會計","zh":"資產","ex":"The building is the company's most valuable asset."},
    {"word":"audit","pos":"n.","cat":"財務會計","zh":"審計、查帳","ex":"The external audit revealed no discrepancies."},
    {"word":"budget","pos":"n.","cat":"財務會計","zh":"預算","ex":"The project is within budget so far."},
    {"word":"comply","pos":"v.","cat":"財務會計","zh":"遵守、符合","ex":"All companies must comply with the new tax regulations."},
    {"word":"deficit","pos":"n.","cat":"財務會計","zh":"赤字、虧損","ex":"The company reported a deficit for the third quarter."},
    {"word":"depreciate","pos":"v.","cat":"財務會計","zh":"折舊、貶值","ex":"Office equipment depreciates over time."},
    {"word":"dividend","pos":"n.","cat":"財務會計","zh":"股息","ex":"Shareholders will receive a dividend of $2 per share."},
    {"word":"expenditure","pos":"n.","cat":"財務會計","zh":"支出、費用","ex":"Total expenditure exceeded the allocated budget."},
    {"word":"fiscal","pos":"adj.","cat":"財務會計","zh":"財政的、會計的","ex":"The fiscal year ends on December 31st."},
    {"word":"invoice","pos":"n.","cat":"財務會計","zh":"發票、請款單","ex":"Please send the invoice to the accounting department."},
    {"word":"liability","pos":"n.","cat":"財務會計","zh":"負債、責任","ex":"Long-term liabilities are listed on the balance sheet."},
    {"word":"overhead","pos":"n.","cat":"財務會計","zh":"管銷費用","ex":"We need to reduce overhead costs this quarter."},
    {"word":"quarterly","pos":"adj.","cat":"財務會計","zh":"每季的","ex":"The quarterly earnings report exceeded expectations."},
    {"word":"revenue","pos":"n.","cat":"財務會計","zh":"收益、營收","ex":"The company reported record revenue this quarter."},
    {"word":"transaction","pos":"n.","cat":"財務會計","zh":"交易","ex":"All transactions must be recorded in the system."},
    {"word":"profitable","pos":"adj.","cat":"財務會計","zh":"有利可圖的","ex":"The new branch proved to be very profitable."},
    {"word":"payable","pos":"adj.","cat":"財務會計","zh":"應付的","ex":"Accounts payable must be settled by month-end."},
    {"word":"receivable","pos":"adj.","cat":"財務會計","zh":"應收的","ex":"Accounts receivable increased by 15% this quarter."},
    # 行銷業務
    {"word":"advertise","pos":"v.","cat":"行銷業務","zh":"廣告、宣傳","ex":"The company decided to advertise on social media."},
    {"word":"brand","pos":"n.","cat":"行銷業務","zh":"品牌","ex":"Building a strong brand takes time and consistency."},
    {"word":"campaign","pos":"n.","cat":"行銷業務","zh":"行銷活動","ex":"The marketing campaign generated impressive results."},
    {"word":"clientele","pos":"n.","cat":"行銷業務","zh":"顧客群","ex":"The store's clientele consists mostly of young professionals."},
    {"word":"distribute","pos":"v.","cat":"行銷業務","zh":"分發、分銷","ex":"We distribute products to over 50 countries."},
    {"word":"endorse","pos":"v.","cat":"行銷業務","zh":"代言、背書","ex":"The athlete was paid to endorse the new sports drink."},
    {"word":"launch","pos":"v.","cat":"行銷業務","zh":"推出、發布","ex":"The company will launch a new product line in spring."},
    {"word":"merchandise","pos":"n.","cat":"行銷業務","zh":"商品","ex":"The store sells a wide variety of merchandise."},
    {"word":"promote","pos":"v.","cat":"行銷業務","zh":"促銷、推廣","ex":"The sale is being promoted through email newsletters."},
    {"word":"retail","pos":"n.","cat":"行銷業務","zh":"零售","ex":"Retail sales increased significantly during the holidays."},
    {"word":"survey","pos":"n.","cat":"行銷業務","zh":"調查","ex":"Please complete the customer satisfaction survey."},
    {"word":"target","pos":"n.","cat":"行銷業務","zh":"目標（群眾）","ex":"The target market for this product is ages 25-40."},
    {"word":"wholesale","pos":"n.","cat":"行銷業務","zh":"批發","ex":"The wholesale price is 30% lower than retail."},
    {"word":"yield","pos":"v.","cat":"行銷業務","zh":"產生（回報）","ex":"The investment yielded a 12% annual return."},
    {"word":"competitive","pos":"adj.","cat":"行銷業務","zh":"有競爭力的","ex":"Our pricing is highly competitive in the market."},
    # 人力資源
    {"word":"applicant","pos":"n.","cat":"人力資源","zh":"申請者、應徵者","ex":"Over 200 applicants responded to the job posting."},
    {"word":"benefit","pos":"n.","cat":"人力資源","zh":"福利","ex":"The company offers excellent employee benefits."},
    {"word":"candidate","pos":"n.","cat":"人力資源","zh":"候選人","ex":"She is the top candidate for the position."},
    {"word":"eligible","pos":"adj.","cat":"人力資源","zh":"符合資格的","ex":"Employees with 5+ years are eligible for the program."},
    {"word":"hire","pos":"v.","cat":"人力資源","zh":"雇用","ex":"We plan to hire ten new staff members this quarter."},
    {"word":"incentive","pos":"n.","cat":"人力資源","zh":"激勵、獎勵","ex":"The bonus serves as an incentive for performance."},
    {"word":"recruit","pos":"v.","cat":"人力資源","zh":"招募","ex":"HR is actively recruiting for the engineering team."},
    {"word":"relocate","pos":"v.","cat":"人力資源","zh":"重新安置、遷移","ex":"The employee agreed to relocate to the new branch."},
    {"word":"resign","pos":"v.","cat":"人力資源","zh":"辭職","ex":"She decided to resign from her position last Friday."},
    {"word":"retire","pos":"v.","cat":"人力資源","zh":"退休","ex":"He plans to retire at the age of 60."},
    {"word":"supervisory","pos":"adj.","cat":"人力資源","zh":"監督的","ex":"This role requires supervisory experience."},
    {"word":"terminate","pos":"v.","cat":"人力資源","zh":"終止（合約）","ex":"The contract was terminated due to poor performance."},
    {"word":"vacancy","pos":"n.","cat":"人力資源","zh":"職缺","ex":"There is a vacancy in the marketing department."},
    {"word":"probationary","pos":"adj.","cat":"人力資源","zh":"試用期的","ex":"New employees serve a three-month probationary period."},
    {"word":"commute","pos":"v.","cat":"人力資源","zh":"通勤","ex":"Many employees commute over an hour each way."},
    # 旅遊交通
    {"word":"adjacent","pos":"adj.","cat":"旅遊交通","zh":"相鄰的","ex":"The conference room is adjacent to the lobby."},
    {"word":"arrival","pos":"n.","cat":"旅遊交通","zh":"抵達","ex":"Please check the arrival time on your boarding pass."},
    {"word":"boarding","pos":"n.","cat":"旅遊交通","zh":"登機、登船","ex":"Boarding will begin 30 minutes before departure."},
    {"word":"connection","pos":"n.","cat":"旅遊交通","zh":"轉機、轉乘","ex":"She missed her connection in Tokyo due to a delay."},
    {"word":"customs","pos":"n.","cat":"旅遊交通","zh":"海關","ex":"All passengers must go through customs upon arrival."},
    {"word":"departure","pos":"n.","cat":"旅遊交通","zh":"出發、離港","ex":"The departure gate has been changed to Gate 12."},
    {"word":"itinerary","pos":"n.","cat":"旅遊交通","zh":"旅程表","ex":"Please send me your itinerary for the business trip."},
    {"word":"layover","pos":"n.","cat":"旅遊交通","zh":"中途停留","ex":"There is a two-hour layover in Singapore."},
    {"word":"reservation","pos":"n.","cat":"旅遊交通","zh":"預訂","ex":"I'd like to confirm my hotel reservation."},
    {"word":"terminal","pos":"n.","cat":"旅遊交通","zh":"航廈、候機樓","ex":"International flights depart from Terminal 2."},
    {"word":"transit","pos":"n.","cat":"旅遊交通","zh":"過境、轉運","ex":"Passengers in transit do not need to collect their baggage."},
    {"word":"turbulence","pos":"n.","cat":"旅遊交通","zh":"亂流","ex":"The pilot advised passengers to fasten seatbelts due to turbulence."},
    {"word":"venue","pos":"n.","cat":"旅遊交通","zh":"會場、場地","ex":"The event venue holds up to 500 guests."},
    # 法律合規
    {"word":"breach","pos":"n.","cat":"法律合規","zh":"違反、違約","ex":"Filing a lawsuit for breach of contract is common."},
    {"word":"clause","pos":"n.","cat":"法律合規","zh":"條款","ex":"Please review the confidentiality clause carefully."},
    {"word":"confidential","pos":"adj.","cat":"法律合規","zh":"機密的","ex":"This document is strictly confidential."},
    {"word":"contract","pos":"n.","cat":"法律合規","zh":"合約","ex":"Both parties signed the contract yesterday."},
    {"word":"dispute","pos":"n.","cat":"法律合規","zh":"爭議、糾紛","ex":"The dispute was resolved through mediation."},
    {"word":"enforce","pos":"v.","cat":"法律合規","zh":"執行（法規）","ex":"The government will enforce the new regulations strictly."},
    {"word":"guarantee","pos":"n.","cat":"法律合規","zh":"保證、擔保","ex":"The product comes with a one-year guarantee."},
    {"word":"liable","pos":"adj.","cat":"法律合規","zh":"有法律責任的","ex":"The company may be liable for damages."},
    {"word":"regulation","pos":"n.","cat":"法律合規","zh":"規定、法規","ex":"All employees must follow safety regulations."},
    {"word":"trademark","pos":"n.","cat":"法律合規","zh":"商標","ex":"The logo is a registered trademark of the company."},
    {"word":"warranty","pos":"n.","cat":"法律合規","zh":"保固","ex":"The warranty covers parts and labor for two years."},
    {"word":"comply","pos":"v.","cat":"法律合規","zh":"遵守","ex":"Failure to comply with regulations may result in fines."},
]

GRAMMAR_QS = [
    {"q":"The report will be submitted _____ Friday.","opts":["on","at","in","by"],"ans":3,"exp":'"By Friday" 表示截止時間，用 by'},
    {"q":"She is responsible _____ managing the budget.","opts":["of","for","to","with"],"ans":1,"exp":'"Responsible for" 是固定搭配'},
    {"q":"The meeting has been _____ until next Monday.","opts":["postponed","cancelled","started","finished"],"ans":0,"exp":'"Postponed until" = 延後到某時間'},
    {"q":"Please _____ the form completely before submitting.","opts":["fill out","fill in","fill up","fill over"],"ans":0,"exp":'"Fill out a form" 填寫表格，美式常用'},
    {"q":"The new policy will _____ effect from January.","opts":["take","do","make","get"],"ans":0,"exp":'"Take effect" = 生效，固定搭配'},
    {"q":"All employees are required to _____ the training.","opts":["attend","join to","participate","enter"],"ans":0,"exp":'"Attend" 不需介系詞'},
    {"q":"The product is currently _____ of stock.","opts":["out","away","off","short"],"ans":0,"exp":'"Out of stock" = 缺貨'},
    {"q":"The contract was signed _____ both parties.","opts":["by","of","from","with"],"ans":0,"exp":"被動語態行為者用 by"},
    {"q":"We need to _____ a decision by end of day.","opts":["make","do","take","have"],"ans":0,"exp":'"Make a decision" 固定搭配'},
    {"q":"The budget _____ approved last week.","opts":["was","were","be","is"],"ans":0,"exp":"過去式被動：was + p.p."},
    {"q":"Sales have increased _____ 20% compared to last year.","opts":["by","at","in","for"],"ans":0,"exp":"增加了百分比用 by"},
    {"q":"The manager asked the team _____ overtime this week.","opts":["to work","working","work","worked"],"ans":0,"exp":"ask sb. to-v 固定結構"},
    {"q":"_____ the bad weather, the outdoor event was cancelled.","opts":["Due to","Because","Since","Despite"],"ans":0,"exp":'"Due to" 後接名詞片語'},
    {"q":"The office will be _____ for renovation next week.","opts":["closed","closing","close","closes"],"ans":0,"exp":"be + p.p. 被動語態"},
    {"q":"She has worked here _____ five years.","opts":["for","since","during","from"],"ans":0,"exp":'"For" 接時間長度'},
    {"q":"The new employee _____ to the team yesterday.","opts":["was introduced","introduced","is introduced","has introduced"],"ans":0,"exp":"過去被動：was + p.p."},
    {"q":"He will notify you _____ soon as the package arrives.","opts":["as","so","very","that"],"ans":0,"exp":'"As soon as" = 一…就…'},
    {"q":"The figures in this report are not _____.","opts":["accurate","accuracy","accurately","accurateness"],"ans":0,"exp":"be 動詞後接形容詞"},
    {"q":"Please submit your application _____ the deadline.","opts":["before","until","during","while"],"ans":0,"exp":'"Before the deadline" = 在截止日前'},
    {"q":"The company's profits _____ steadily over the past year.","opts":["have grown","grew","are growing","had grown"],"ans":0,"exp":"現在完成式：持續到現在的結果"},
    {"q":"_____ completing the training, employees receive a certificate.","opts":["Upon","For","By","After"],"ans":0,"exp":'"Upon completing" = 完成後立即'},
    {"q":"The document needs to be _____ before distribution.","opts":["proofread","proofreading","to proofread","proofread by"],"ans":0,"exp":"need to be + p.p. 被動不定詞"},
    {"q":"Please let me know if you have _____ questions.","opts":["any","some","many","few"],"ans":0,"exp":"疑問或條件句中用 any"},
    {"q":"The seminar will be held _____ the third floor.","opts":["on","in","at","by"],"ans":0,"exp":"樓層用 on（在幾樓）"},
    {"q":"Sales _____ by 15% if we launch the new product.","opts":["will increase","would increase","increase","are increasing"],"ans":0,"exp":"真實條件句：if + 現在式，主句用 will"},
    {"q":"The CEO will _____ the annual shareholders' meeting.","opts":["address","speech","talk","speak"],"ans":0,"exp":'"Address the meeting" = 在會議上發言'},
    {"q":"The project is behind schedule _____ unexpected delays.","opts":["due to","because","so","however"],"ans":0,"exp":'"Due to" 後接名詞'},
    {"q":"Employees must _____ with the company's dress code.","opts":["comply","agreement","follow with","obey to"],"ans":0,"exp":'"Comply with" = 遵守（固定搭配）'},
    {"q":"The report was _____ prepared by the marketing team.","opts":["thoroughly","thorough","thoroughness","thorough in"],"ans":0,"exp":"修飾動詞用副詞 thoroughly"},
    {"q":"Please _____ your supervisor before making any changes.","opts":["consult","consult with","consulting","consulted"],"ans":0,"exp":'"Consult" 可直接接受詞'},
]

LISTEN_P2 = [
    {"q":"When will the budget report be ready?","opts":["A. It's on the third shelf.","B. By Thursday afternoon.","C. The budget was approved."],"ans":1,"exp":"問何時，答 By Thursday 最符合"},
    {"q":"Who is in charge of the marketing campaign?","opts":["A. Ms. Chen is leading it.","B. The campaign starts in May.","C. We have a new product."],"ans":0,"exp":"問人，答 Ms. Chen 最直接"},
    {"q":"Has the client confirmed the meeting time?","opts":["A. Yes, two o'clock is fine.","B. The client is very satisfied.","C. The meeting room is available."],"ans":0,"exp":"Yes/No 問句，A 最合適"},
    {"q":"Where should I submit the expense report?","opts":["A. It was submitted yesterday.","B. To the accounting department.","C. The report is very detailed."],"ans":1,"exp":"問 where，答地點"},
    {"q":"Why was the project deadline extended?","opts":["A. The deadline is Friday.","B. Because of unexpected technical issues.","C. The project was very successful."],"ans":1,"exp":"問 why，答 Because 最合適"},
    {"q":"Could you send me the revised contract?","opts":["A. Sure, I'll email it right away.","B. The contract was signed.","C. I don't have a contract."],"ans":0,"exp":"請求，A 表示同意最合適"},
    {"q":"When does the new employee orientation begin?","opts":["A. The orientation was very helpful.","B. It begins at nine tomorrow morning.","C. There are five new employees."],"ans":1,"exp":"問何時，答具體時間"},
    {"q":"How many people attended the conference?","opts":["A. The conference was in Tokyo.","B. About 300 participants.","C. It lasted three days."],"ans":1,"exp":"問數量，答約 300 人"},
    {"q":"Is the printer on the second floor working?","opts":["A. I printed ten copies.","B. No, it's being repaired.","C. The printer is expensive."],"ans":1,"exp":"Yes/No 問句，B 最合適"},
    {"q":"Who should I contact about the IT issue?","opts":["A. Call the IT help desk.","B. The IT department is on Floor 3.","C. The issue was resolved."],"ans":0,"exp":"問聯絡對象，A 直接回答"},
]

LISTEN_P3 = [
    {
        "title":"對話 1：預約會議室",
        "lines":[
            "M: Hi, I need to book the large conference room for Friday afternoon.",
            "W: Let me check the schedule. I'm sorry, it's already reserved from 2 to 5 PM.",
            "M: How about in the morning? Say, from 9 to 11?",
            "W: That's available. Shall I reserve it for you now?",
            "M: Yes, please. It's for the sales team's quarterly review."
        ],
        "qs":[
            {"q":"What does the man want to do?","opts":["Book a conference room","Cancel a reservation","Check the schedule","Move a meeting"],"ans":0},
            {"q":"Why is the large room unavailable in the afternoon?","opts":["It is being renovated","It is already reserved","It is too small","It is closed for cleaning"],"ans":1},
            {"q":"What time will the man's meeting be held?","opts":["9 to 11 AM","2 to 5 PM","1 to 3 PM","All day"],"ans":0},
        ]
    },
    {
        "title":"對話 2：訂購辦公用品",
        "lines":[
            "W: I noticed we're running low on printer paper and toner cartridges.",
            "M: You're right. I'll put in an order this afternoon.",
            "W: Could you also add some pens and sticky notes to the order?",
            "M: Sure. Do you need anything else for your department?",
            "W: That should be enough. Oh, and please get express shipping — we need them by Wednesday."
        ],
        "qs":[
            {"q":"What is the main topic of the conversation?","opts":["A broken printer","Ordering office supplies","Hiring new staff","Planning a meeting"],"ans":1},
            {"q":"What kind of shipping does the woman request?","opts":["Standard","Express","Overnight","Free"],"ans":1},
            {"q":"When do they need the supplies?","opts":["Monday","Tuesday","Wednesday","Friday"],"ans":2},
        ]
    },
]

LISTEN_P4 = [
    {
        "title":"獨白 1：機場廣播",
        "text":"Attention, passengers on Flight KA 305 to Singapore. Due to a technical issue, boarding will be delayed by approximately 45 minutes. The new boarding time is 3:30 PM at Gate 22. Passengers requiring special assistance should proceed to the gate immediately. We apologize for the inconvenience and thank you for your patience.",
        "qs":[
            {"q":"Why is the flight delayed?","opts":["Bad weather","A technical issue","Gate change","Staff shortage"],"ans":1},
            {"q":"What is the new boarding time?","opts":["3:00 PM","3:15 PM","3:30 PM","4:00 PM"],"ans":2},
            {"q":"Who is asked to go to the gate immediately?","opts":["All passengers","Business class only","Passengers needing special help","Frequent flyers"],"ans":2},
        ]
    },
    {
        "title":"獨白 2：公司廣播",
        "text":"Good morning, everyone. This is a reminder that the annual company picnic will be held this Saturday at Riverside Park, starting at 10 AM. All employees and their families are welcome. Please bring your own chairs and sunscreen. Lunch will be provided by the company. If you haven't signed up yet, please contact HR by tomorrow afternoon.",
        "qs":[
            {"q":"What event is being announced?","opts":["A company meeting","An annual picnic","A training seminar","An award ceremony"],"ans":1},
            {"q":"What should employees bring?","opts":["Food and drinks","Their own chairs","Company ID","A laptop"],"ans":1},
            {"q":"By when should employees sign up?","opts":["This morning","Tomorrow afternoon","Saturday morning","End of this week"],"ans":1},
        ]
    },
]

READINGS = [
    {
        "title":"Email: Project Status Update",
        "text":"""To: All Project Team Members
From: Sarah Chen, Project Manager
Subject: Q3 Project Update

Dear Team,

I wanted to share a brief update on the status of our Q3 initiative. As of this week, we have completed 75% of the planned deliverables. The development phase is on track, and we expect to finish by the end of next week.

However, the testing phase is slightly behind schedule due to some unexpected technical issues. To address this, I have arranged for additional QA support starting Monday. All team members should receive updated timelines by Thursday.

Please let me know if you have any questions or concerns.

Best regards,
Sarah Chen""",
        "qs":[
            {"q":"What percentage of deliverables is complete?","opts":["50%","65%","75%","90%"],"ans":2},
            {"q":"Why is the testing phase behind schedule?","opts":["Lack of staff","Technical issues","Budget cuts","Poor planning"],"ans":1},
            {"q":"What will team members receive by Thursday?","opts":["New assignments","Updated timelines","Performance reviews","Budget reports"],"ans":1},
            {"q":"The word 'initiative' is closest in meaning to:","opts":["Problem","Project","Meeting","Policy"],"ans":1},
        ]
    },
    {
        "title":"Notice: Office Renovation",
        "text":"""OFFICE RENOVATION NOTICE

To all staff:

Please be advised that the third floor will undergo renovation from June 10 to June 25. During this period, all staff currently located on the third floor will be temporarily relocated to available workstations on floors two and four.

Access to the third floor will be restricted to authorized personnel only. The elevators will remain operational; however, the stairwell near the east exit will be closed for safety reasons.

IT support will assist with equipment setup in the temporary locations. For questions, please contact facilities management at ext. 305.

Management""",
        "qs":[
            {"q":"Which floor is being renovated?","opts":["Second","Third","Fourth","All floors"],"ans":1},
            {"q":"Where will affected staff be moved?","opts":["To another building","Floors 2 and 4","To work from home","The basement"],"ans":1},
            {"q":"What will be closed during renovation?","opts":["The elevators","The parking lot","The east stairwell","The main entrance"],"ans":2},
            {"q":"Who should staff contact for questions?","opts":["HR department","IT support","Facilities management","The CEO"],"ans":2},
        ]
    },
    {
        "title":"Advertisement: Job Opening",
        "text":"""HIRING: Senior Marketing Manager

XYZ Corporation is seeking a talented Senior Marketing Manager to join our growing team in Taipei.

Responsibilities:
• Develop and execute integrated marketing campaigns
• Manage a team of 5 marketing specialists
• Analyze market trends and report to senior leadership
• Oversee social media strategy and content creation

Requirements:
• Bachelor's degree in Marketing or related field
• Minimum 7 years of marketing experience
• Strong leadership and communication skills
• Fluent in English and Mandarin

Salary: Competitive, based on experience
Benefits: Health insurance, annual bonus, flexible hours

To apply, send your resume and cover letter to careers@xyzgroup.com by July 15.""",
        "qs":[
            {"q":"How many specialists will the manager oversee?","opts":["3","5","7","10"],"ans":1},
            {"q":"What language skill is required?","opts":["Japanese","English only","English and Mandarin","Mandarin only"],"ans":2},
            {"q":"Which of the following is NOT listed as a requirement?","opts":["Leadership skills","7 years experience","MBA degree","Marketing background"],"ans":2},
            {"q":"By when must applications be submitted?","opts":["June 30","July 1","July 15","July 31"],"ans":2},
        ]
    },
    {
        "title":"Memo: Remote Work Policy",
        "text":"""MEMORANDUM

To: All Employees
From: Human Resources
Re: Updated Remote Work Policy
Date: May 1

Effective June 1, the company will implement a hybrid work model. Employees may work remotely up to three days per week, provided they maintain full productivity and attend all scheduled meetings.

Remote workdays must be approved by the direct supervisor at least 48 hours in advance. Employees working remotely are expected to be available during core hours (9 AM – 3 PM) and respond to communications within one hour.

All remote workers must use the company VPN and ensure a secure, professional work environment. Employees who do not comply with this policy may lose remote work privileges.

For more details, please refer to the full policy document on the company intranet.""",
        "qs":[
            {"q":"When does the new policy take effect?","opts":["May 1","June 1","July 1","Immediately"],"ans":1},
            {"q":"How many remote days per week are allowed?","opts":["1","2","3","5"],"ans":2},
            {"q":"How far in advance must remote days be approved?","opts":["24 hours","48 hours","One week","Same day"],"ans":1},
            {"q":"What tool must remote workers use?","opts":["A company phone","The company VPN","A time tracker","Video conferencing"],"ans":2},
        ]
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 狀態管理
# ─────────────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "learned": set(),
        "correct": 0,
        "total": 0,
        "sessions": 0,
        "mistakes": [],
        # 單字卡
        "v_idx": 0,
        "v_flipped": False,
        "v_cat": "全部",
        # 文法
        "g_qs": [],
        "g_idx": 0,
        "g_done": {},
        "g_started": False,
        # 聽力
        "lp2_idx": 0,
        "lp3_idx": 0,
        "lp3_q": 0,
        "lp4_idx": 0,
        "lp4_q": 0,
        # 閱讀
        "r_idx": 0,
        "r_done": {},
        # 模擬考
        "mock_qs": [],
        "mock_idx": 0,
        "mock_done": {},
        "mock_started": False,
        "mock_end_time": 0.0,
        "mock_finished": False,
        # 錯題複習
        "rev_idx": 0,
        "rev_done": {},
        # 單字庫搜尋
        "wl_query": "",
        "wl_cat": "全部",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
S = st.session_state

# ─────────────────────────────────────────────────────────────────────────────
# 工具函式
# ─────────────────────────────────────────────────────────────────────────────
def est_toeic():
    if S.total == 0:
        return "—"
    acc = S.correct / S.total
    if acc >= 0.95: return "950+"
    if acc >= 0.87: return "~880"
    if acc >= 0.78: return "~790 ✨"
    if acc >= 0.68: return "~700"
    if acc >= 0.58: return "~620"
    return "~520"

def add_mistake(type_, q, correct, chosen):
    S.mistakes.append({"type": type_, "q": q, "correct": correct, "chosen": chosen})
    if len(S.mistakes) > 100:
        S.mistakes.pop(0)

def vocab_filtered():
    cat = S.v_cat
    if cat == "全部":
        return VOCAB
    return [w for w in VOCAB if w["cat"] == cat]

def gen_mcq(w):
    same_pos = [x for x in VOCAB if x["pos"] == w["pos"] and x["word"] != w["word"]]
    wrongs = random.sample(same_pos, min(3, len(same_pos)))
    opts = [w["word"]] + [x["word"] for x in wrongs]
    random.shuffle(opts)
    return {"q": f"Choose the correct word: {w['zh']} ({w['pos']})", "opts": opts, "ans": opts.index(w["word"]), "word": w}

def speak_js(text):
    safe = text.replace("'", "\\'").replace("\n", " ")
    components.html(f"""
    <script>
    (function(){{
      var u = new SpeechSynthesisUtterance('{safe}');
      u.lang = 'en-US'; u.rate = 0.88; u.pitch = 1;
      window.speechSynthesis.cancel();
      var voices = window.speechSynthesis.getVoices();
      var en = voices.find(v => v.lang.startsWith('en'));
      if (en) u.voice = en;
      window.speechSynthesis.speak(u);
    }})();
    </script>
    """, height=0)

def tag_html(pos):
    cls = {"n.": "tag-n", "v.": "tag-v", "adj.": "tag-adj", "adv.": "tag-adv"}.get(pos, "tag-n")
    return f'<span class="tag {cls}">{pos}</span>'

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：首頁儀表板
# ─────────────────────────────────────────────────────────────────────────────
def page_home():
    st.markdown("""
    <div class="hero">
      <h1>🎯 TOEIC Pro 750+</h1>
      <p>系統化備考，穩定達成多益 750 分目標</p>
    </div>
    """, unsafe_allow_html=True)

    acc = f"{S.correct/S.total*100:.0f}%" if S.total > 0 else "—"
    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-box"><div class="stat-num">{len(S.learned)}</div><div class="stat-lbl">📚 已學單字</div></div>
      <div class="stat-box"><div class="stat-num">{acc}</div><div class="stat-lbl">🎯 整體正確率</div></div>
      <div class="stat-box"><div class="stat-num">{S.sessions}</div><div class="stat-lbl">✅ 練習次數</div></div>
      <div class="stat-box"><div class="stat-num">{len(S.mistakes)}</div><div class="stat-lbl">🔴 待複習錯題</div></div>
      <div class="stat-box"><div class="stat-num">{est_toeic()}</div><div class="stat-lbl">📊 預估多益分數</div></div>
    </div>
    """, unsafe_allow_html=True)

    if S.total > 0:
        pct = S.correct / S.total
        st.markdown(f"""
        <div class="tcard">
          <b>整體進度</b>　{S.correct}/{S.total} 題正確
          <div class="pb-wrap"><div class="pb" style="width:{pct*100:.0f}%"></div></div>
          <small style="color:#64748b">目標：78% 以上 → 預估 750+</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📚 學習路線建議")
    st.info("""
**第 1-2 週：建立基礎**
- 每天完成 1 輪單字卡（全部 120 個）
- 完成文法測驗 1 次，複習錯題

**第 3-4 週：強化弱點**
- 針對正確率低的分項加強
- 每天聽力練習（Part 2 → Part 3 → Part 4）
- 閱讀全部 4 篇文章

**第 5-6 週：模擬考衝刺**
- 每天一次計時模擬考（50 題 / 30 分）
- 複習所有錯題，正確率達 78% → 預估 750+
    """)

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：單字卡
# ─────────────────────────────────────────────────────────────────────────────
def page_vocab():
    st.markdown("## 📚 單字卡練習")
    cats = ["全部"] + sorted(set(w["cat"] for w in VOCAB))
    S.v_cat = st.selectbox("分類篩選", cats, index=cats.index(S.v_cat))
    words = vocab_filtered()

    if not words:
        st.warning("此分類無單字")
        return

    if S.v_idx >= len(words):
        S.v_idx = 0

    total_w = len(words)
    done_w = len([w for w in words if w["word"] in S.learned])
    st.markdown(f"""
    <div class="pb-wrap"><div class="pb" style="width:{done_w/total_w*100:.0f}%"></div></div>
    <small style="color:#64748b">已學 {done_w}/{total_w}　第 {S.v_idx+1}/{total_w} 張</small>
    """, unsafe_allow_html=True)

    w = words[S.v_idx]
    flipped = S.v_flipped

    if not flipped:
        st.markdown(f"""
        <div class="flashcard">
          <div class="fc-word">{w['word']}</div>
          <div class="fc-pos">{w['pos']} ‧ {w['cat']}</div>
          <div style="margin-top:1rem;font-size:.85rem;opacity:.7">點擊「翻牌」查看意思</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="flashcard" style="background:linear-gradient(135deg,#059669,#047857)">
          <div class="fc-zh">{w['zh']}</div>
          <div class="fc-ex">"{w['ex']}"</div>
        </div>
        """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🔊 發音", use_container_width=True):
            speak_js(w["word"] + ". " + w["ex"])
    with c2:
        if st.button("翻牌 🔄" if not flipped else "收起 🔄", use_container_width=True):
            S.v_flipped = not S.v_flipped
            st.rerun()
    with c3:
        if st.button("✅ 已學會", use_container_width=True):
            S.learned.add(w["word"])
            S.v_idx = (S.v_idx + 1) % len(words)
            S.v_flipped = False
            st.rerun()
    with c4:
        if st.button("➡️ 下一張", use_container_width=True):
            S.v_idx = (S.v_idx + 1) % len(words)
            S.v_flipped = False
            st.rerun()

    st.markdown("---")
    with st.expander("🔀 隨機跳至其他單字"):
        if st.button("隨機一張"):
            S.v_idx = random.randint(0, len(words) - 1)
            S.v_flipped = False
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：文法測驗
# ─────────────────────────────────────────────────────────────────────────────
def page_grammar():
    st.markdown("## 📝 文法測驗（Part 5）")

    if not S.g_started:
        st.info(f"共 {len(GRAMMAR_QS)} 題，涵蓋時態、介系詞、詞性辨別、固定片語等考點。")
        if st.button("▶️ 開始測驗", type="primary"):
            S.g_qs = random.sample(GRAMMAR_QS, len(GRAMMAR_QS))
            S.g_idx = 0
            S.g_done = {}
            S.g_started = True
            S.sessions += 1
            st.rerun()
        return

    qs = S.g_qs
    idx = S.g_idx
    done = S.g_done

    # 完成
    if idx >= len(qs):
        correct = sum(1 for k, v in done.items() if v["ok"])
        acc = correct / len(qs) * 100
        st.success(f"### 測驗完成！正確率 {acc:.0f}%  ({correct}/{len(qs)})")
        S.correct += correct
        S.total += len(qs)
        if st.button("🔄 再來一次"):
            S.g_started = False
            st.rerun()
        st.markdown("#### 錯題回顧")
        for k, v in done.items():
            if not v["ok"]:
                q = qs[int(k)]
                with st.expander(f"❌ Q{int(k)+1}: {q['q']}"):
                    st.error(f"你選了：{q['opts'][v['chosen']]}")
                    st.success(f"正確答案：{q['opts'][q['ans']]}")
                    st.info(f"💡 解析：{q['exp']}")
        return

    q = qs[idx]
    answered = str(idx) in done

    pct = idx / len(qs)
    st.markdown(f"""
    <div class="pb-wrap"><div class="pb" style="width:{pct*100:.0f}%"></div></div>
    <small style="color:#64748b">第 {idx+1}/{len(qs)} 題</small>
    """, unsafe_allow_html=True)

    st.markdown(f"<div class='tcard'><b>Q{idx+1}.</b> {q['q']}</div>", unsafe_allow_html=True)

    for i, opt in enumerate(q["opts"]):
        label = f"{chr(65+i)}. {opt}"
        if answered:
            v = done[str(idx)]
            if i == q["ans"]:
                st.markdown(f"<div style='background:#ecfdf5;border:2px solid #10b981;border-radius:10px;padding:.6rem 1rem;margin:.3rem 0'>✅ {label}</div>", unsafe_allow_html=True)
            elif i == v["chosen"]:
                st.markdown(f"<div style='background:#fef2f2;border:2px solid #ef4444;border-radius:10px;padding:.6rem 1rem;margin:.3rem 0'>❌ {label}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:.6rem 1rem;margin:.3rem 0;color:#64748b'>{label}</div>", unsafe_allow_html=True)
        else:
            if st.button(label, key=f"g_{idx}_{i}", use_container_width=True):
                ok = (i == q["ans"])
                done[str(idx)] = {"chosen": i, "ok": ok}
                if not ok:
                    add_mistake("grammar", q["q"], q["opts"][q["ans"]], q["opts"][i])
                st.rerun()

    if answered:
        v = done[str(idx)]
        if v["ok"]:
            st.markdown('<div class="fb-ok">✅ 答對了！' + q["exp"] + '</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fb-bad">❌ 答錯了。正確：<b>' + q["opts"][q["ans"]] + '</b><br>💡 ' + q["exp"] + '</div>', unsafe_allow_html=True)
        if st.button("下一題 →", type="primary"):
            S.g_idx += 1
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：聽力練習
# ─────────────────────────────────────────────────────────────────────────────
def page_listening():
    st.markdown("## 🎧 聽力練習")
    st.info("請確認瀏覽器已允許音訊，點擊「播放」後系統將朗讀題目。", icon="🔊")

    tab1, tab2, tab3 = st.tabs(["Part 2 應答題", "Part 3 對話題", "Part 4 獨白題"])

    with tab1:
        st.markdown(f"**Part 2：聽一個問句，選出最佳回應** （共 {len(LISTEN_P2)} 題）")
        idx = S.lp2_idx
        if idx >= len(LISTEN_P2):
            st.success("Part 2 全部完成！")
            if st.button("🔄 重新練習", key="p2_reset"):
                S.lp2_idx = 0; st.rerun()
        else:
            item = LISTEN_P2[idx]
            pct = idx / len(LISTEN_P2)
            st.markdown(f'<div class="pb-wrap"><div class="pb" style="width:{pct*100:.0f}%"></div></div><small>第 {idx+1}/{len(LISTEN_P2)} 題</small>', unsafe_allow_html=True)
            st.markdown(f"<div class='tcard'>🎧 **題目：** {item['q']}</div>", unsafe_allow_html=True)
            if st.button("▶️ 播放題目", key=f"p2_speak_{idx}"):
                speak_js(item["q"])
            for i, opt in enumerate(item["opts"]):
                if st.button(opt, key=f"p2_{idx}_{i}", use_container_width=True):
                    ok = (i == item["ans"])
                    S.correct += (1 if ok else 0)
                    S.total += 1
                    if not ok:
                        add_mistake("listen_p2", item["q"], item["opts"][item["ans"]], opt)
                    S.sessions += 1
                    if ok:
                        st.success(f"✅ 正確！解析：{item['exp']}")
                    else:
                        st.error(f"❌ 答錯。正確：{item['opts'][item['ans']]}  解析：{item['exp']}")
                    if st.button("下一題 →", key=f"p2_next_{idx}"):
                        S.lp2_idx += 1; st.rerun()

    with tab2:
        st.markdown("**Part 3：聽對話，回答問題**（共 2 段對話）")
        idx3 = S.lp3_idx
        if idx3 >= len(LISTEN_P3):
            st.success("Part 3 全部完成！")
            if st.button("🔄 重新練習", key="p3_reset"):
                S.lp3_idx = 0; S.lp3_q = 0; st.rerun()
        else:
            conv = LISTEN_P3[idx3]
            st.markdown(f"#### {conv['title']}")
            with st.expander("📄 對話內容（建議先聽再看）"):
                for line in conv["lines"]:
                    st.write(line)
            if st.button("▶️ 播放對話", key=f"p3_speak_{idx3}"):
                speak_js(" ... ".join(conv["lines"]))
            st.markdown("---")
            q_idx = S.lp3_q
            if q_idx < len(conv["qs"]):
                q = conv["qs"][q_idx]
                st.markdown(f"**Q{q_idx+1}. {q['q']}**")
                for i, opt in enumerate(q["opts"]):
                    if st.button(f"{chr(65+i)}. {opt}", key=f"p3_{idx3}_{q_idx}_{i}", use_container_width=True):
                        ok = (i == q["ans"])
                        S.correct += (1 if ok else 0); S.total += 1
                        if not ok:
                            add_mistake("listen_p3", q["q"], q["opts"][q["ans"]], opt)
                        if ok: st.success("✅ 正確！")
                        else: st.error(f"❌ 正確答案：{q['opts'][q['ans']]}")
                        if st.button("下一題 →", key=f"p3_nxt_{idx3}_{q_idx}"):
                            if q_idx + 1 >= len(conv["qs"]):
                                S.lp3_idx += 1; S.lp3_q = 0
                            else:
                                S.lp3_q += 1
                            st.rerun()

    with tab3:
        st.markdown("**Part 4：聽獨白，回答問題**（共 2 篇）")
        idx4 = S.lp4_idx
        if idx4 >= len(LISTEN_P4):
            st.success("Part 4 全部完成！")
            if st.button("🔄 重新練習", key="p4_reset"):
                S.lp4_idx = 0; S.lp4_q = 0; st.rerun()
        else:
            passage = LISTEN_P4[idx4]
            st.markdown(f"#### {passage['title']}")
            with st.expander("📄 獨白內容"):
                st.write(passage["text"])
            if st.button("▶️ 播放獨白", key=f"p4_speak_{idx4}"):
                speak_js(passage["text"])
            st.markdown("---")
            q_idx = S.lp4_q
            if q_idx < len(passage["qs"]):
                q = passage["qs"][q_idx]
                st.markdown(f"**Q{q_idx+1}. {q['q']}**")
                for i, opt in enumerate(q["opts"]):
                    if st.button(f"{chr(65+i)}. {opt}", key=f"p4_{idx4}_{q_idx}_{i}", use_container_width=True):
                        ok = (i == q["ans"])
                        S.correct += (1 if ok else 0); S.total += 1
                        if not ok:
                            add_mistake("listen_p4", q["q"], q["opts"][q["ans"]], opt)
                        if ok: st.success("✅ 正確！")
                        else: st.error(f"❌ 正確答案：{q['opts'][q['ans']]}")
                        if st.button("下一題 →", key=f"p4_nxt_{idx4}_{q_idx}"):
                            if q_idx + 1 >= len(passage["qs"]):
                                S.lp4_idx += 1; S.lp4_q = 0
                            else:
                                S.lp4_q += 1
                            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：閱讀測驗
# ─────────────────────────────────────────────────────────────────────────────
def page_reading():
    st.markdown("## 📖 閱讀測驗（Part 7）")
    arts = READINGS
    idx = S.r_idx
    done = S.r_done

    art_names = [f"{'✅' if str(i) in done and len(done[str(i)]) == len(arts[i]['qs']) else '📄'} {arts[i]['title']}" for i in range(len(arts))]
    selected = st.selectbox("選擇文章", art_names, index=idx)
    new_idx = art_names.index(selected)
    if new_idx != S.r_idx:
        S.r_idx = new_idx
        st.rerun()

    art = arts[idx]
    st.markdown(f"#### {art['title']}")
    with st.expander("📄 閱讀文章", expanded=True):
        st.text(art["text"])

    st.markdown("---")
    art_done = done.get(str(idx), {})

    for qi, q in enumerate(art["qs"]):
        st.markdown(f"**Q{qi+1}. {q['q']}**")
        answered = str(qi) in art_done
        for i, opt in enumerate(q["opts"]):
            label = f"{chr(65+i)}. {opt}"
            if answered:
                if i == q["ans"]:
                    st.markdown(f'<div style="background:#ecfdf5;border:2px solid #10b981;border-radius:8px;padding:.5rem 1rem;margin:.25rem 0">✅ {label}</div>', unsafe_allow_html=True)
                elif i == art_done[str(qi)]:
                    st.markdown(f'<div style="background:#fef2f2;border:2px solid #ef4444;border-radius:8px;padding:.5rem 1rem;margin:.25rem 0">❌ {label}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:.5rem 1rem;margin:.25rem 0;color:#94a3b8">{label}</div>', unsafe_allow_html=True)
            else:
                if st.button(label, key=f"r_{idx}_{qi}_{i}", use_container_width=True):
                    if str(idx) not in done:
                        done[str(idx)] = {}
                    done[str(idx)][str(qi)] = i
                    ok = (i == q["ans"])
                    S.correct += (1 if ok else 0)
                    S.total += 1
                    if not ok:
                        add_mistake("reading", q["q"], q["opts"][q["ans"]], opt)
                    st.rerun()
        st.markdown("")

    answered_count = len(art_done)
    total_q = len(art["qs"])
    if answered_count == total_q:
        correct_count = sum(1 for qi2, i2 in art_done.items() if i2 == art["qs"][int(qi2)]["ans"])
        st.success(f"✅ 本篇完成！正確率 {correct_count}/{total_q}")
        if idx + 1 < len(arts):
            if st.button("▶️ 下一篇文章"):
                S.r_idx += 1
                st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：計時模擬考
# ─────────────────────────────────────────────────────────────────────────────
def page_mock():
    st.markdown("## ⏱ 計時模擬考")
    MOCK_TIME = 30 * 60  # 30 分鐘

    def build_mock_qs():
        qs = []
        g_sample = random.sample(GRAMMAR_QS, min(20, len(GRAMMAR_QS)))
        for q in g_sample:
            qs.append({**q, "source": "grammar"})
        r_qs = []
        for art in READINGS:
            for qi, q in enumerate(art["qs"]):
                r_qs.append({**q, "source": "reading", "article": art["title"]})
        for q in random.sample(r_qs, min(20, len(r_qs))):
            qs.append(q)
        v_sample = random.sample(VOCAB, min(10, len(VOCAB)))
        for w in v_sample:
            mcq = gen_mcq(w)
            qs.append({**mcq, "source": "vocab"})
        random.shuffle(qs)
        return qs

    if not S.mock_started:
        st.info("📋 **考試說明**\n- 共 50 題（文法 20 題、閱讀 20 題、單字 10 題）\n- 限時 **30 分鐘**\n- 計時開始後無法暫停")
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("▶️ 開始模擬考", type="primary"):
                S.mock_qs = build_mock_qs()
                S.mock_idx = 0
                S.mock_done = {}
                S.mock_started = True
                S.mock_end_time = time.time() + MOCK_TIME
                S.mock_finished = False
                S.sessions += 1
                st.rerun()
        return

    if S.mock_finished or S.mock_idx >= len(S.mock_qs):
        _show_mock_result()
        return

    remaining = S.mock_end_time - time.time()
    if remaining <= 0:
        S.mock_finished = True
        st.rerun()

    mins = int(remaining // 60)
    secs = int(remaining % 60)
    timer_class = "timer-box"
    if remaining < 300:
        timer_class += " timer-danger"
    elif remaining < 600:
        timer_class += " timer-warn"

    st.markdown(f'<div class="{timer_class}">⏱ {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

    pct = (len(S.mock_done) / len(S.mock_qs))
    st.markdown(f'<div class="pb-wrap"><div class="pb" style="width:{pct*100:.0f}%"></div></div><small>已作答 {len(S.mock_done)}/{len(S.mock_qs)} 題</small>', unsafe_allow_html=True)

    idx = S.mock_idx
    qs = S.mock_qs

    # 跳過已答
    while idx < len(qs) and str(idx) in S.mock_done:
        idx += 1
    if idx >= len(qs):
        S.mock_finished = True
        st.rerun()

    S.mock_idx = idx
    q = qs[idx]

    source_label = {"grammar": "📝 文法", "reading": "📖 閱讀", "vocab": "📚 單字"}.get(q["source"], "")
    st.markdown(f"<div class='tcard'><small style='color:#64748b'>{source_label} ‧ Q{idx+1}/{len(qs)}</small><br><b>{q['q']}</b></div>", unsafe_allow_html=True)

    if q.get("article"):
        with st.expander("📄 查看相關文章"):
            for art in READINGS:
                if art["title"] == q["article"]:
                    st.text(art["text"])

    for i, opt in enumerate(q["opts"]):
        if st.button(f"{chr(65+i)}. {opt}", key=f"mock_{idx}_{i}", use_container_width=True):
            S.mock_done[str(idx)] = i
            S.mock_idx = idx + 1
            st.rerun()

    c1, c2 = st.columns([1, 4])
    with c1:
        if st.button("⏹ 交卷", type="secondary"):
            S.mock_finished = True
            st.rerun()
    with c2:
        st.caption("作答後自動跳下一題；可點「交卷」提前結束")

    time.sleep(1)
    st.rerun()

def _show_mock_result():
    qs = S.mock_qs
    done = S.mock_done
    correct = sum(1 for k, v in done.items() if v == qs[int(k)]["ans"])
    total_a = len(done)
    acc = correct / len(qs) * 100

    S.correct += correct
    S.total += len(qs)
    S.mock_started = False

    est = "950+" if acc >= 95 else "~880" if acc >= 87 else "~790 ✨" if acc >= 78 else "~700" if acc >= 68 else "~620" if acc >= 58 else "~520"

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#2563eb,#7c3aed);color:white;border-radius:16px;padding:2rem;text-align:center;margin-bottom:1rem">
      <div style="font-size:3rem;font-weight:900">{acc:.0f}%</div>
      <div style="font-size:1.3rem;margin:.5rem 0">預估多益分數：{est}</div>
      <div style="opacity:.85">正確 {correct}/{len(qs)} 題　作答 {total_a} 題</div>
    </div>
    """, unsafe_allow_html=True)

    by_source = {"grammar": [0, 0], "reading": [0, 0], "vocab": [0, 0]}
    for k, v in done.items():
        q = qs[int(k)]
        src = q.get("source", "grammar")
        by_source[src][1] += 1
        if v == q["ans"]:
            by_source[src][0] += 1

    c1, c2, c3 = st.columns(3)
    for col, (src, lbl) in zip([c1, c2, c3], [("grammar", "📝 文法"), ("reading", "📖 閱讀"), ("vocab", "📚 單字")]):
        corr, tot = by_source[src]
        a = f"{corr/tot*100:.0f}%" if tot > 0 else "—"
        with col:
            st.metric(lbl, a, f"{corr}/{tot}")

    if st.button("🔄 重新考一次", type="primary"):
        S.mock_started = False
        S.mock_finished = False
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：錯題複習
# ─────────────────────────────────────────────────────────────────────────────
def page_review():
    st.markdown("## 🔴 錯題複習")

    mistakes = S.mistakes
    if not mistakes:
        st.success("🎉 目前沒有錯題！繼續保持！")
        return

    st.info(f"共 {len(mistakes)} 道待複習錯題")

    idx = S.rev_idx
    done = S.rev_done

    if idx >= len(mistakes):
        correct = sum(1 for v in done.values() if v)
        st.success(f"✅ 本輪複習完成！重新答對 {correct}/{len(mistakes)} 題")
        if st.button("🔄 再複習一次"):
            S.rev_idx = 0; S.rev_done = {}; st.rerun()
        if st.button("🗑️ 清除所有錯題"):
            S.mistakes = []; S.rev_idx = 0; S.rev_done = {}; st.rerun()
        return

    pct = idx / len(mistakes)
    st.markdown(f'<div class="pb-wrap"><div class="pb" style="width:{pct*100:.0f}%"></div></div><small>第 {idx+1}/{len(mistakes)} 題</small>', unsafe_allow_html=True)

    m = mistakes[idx]
    answered = str(idx) in done

    type_label = {"grammar": "📝 文法", "reading": "📖 閱讀", "listen_p2": "🎧 聽力 Part2",
                  "listen_p3": "🎧 聽力 Part3", "listen_p4": "🎧 聽力 Part4", "vocab": "📚 單字"}.get(m["type"], "題目")

    st.markdown(f"<div class='tcard'><small style='color:#ef4444'>{type_label} 錯題</small><br><b>{m['q']}</b></div>", unsafe_allow_html=True)

    if not answered:
        opts = list({m["correct"], m["chosen"]} | set(
            random.sample([w["word"] for w in VOCAB if w["word"] not in {m["correct"], m["chosen"]}], min(2, len(VOCAB)))
        ))
        random.shuffle(opts)

        for opt in opts:
            if st.button(opt, key=f"rev_{idx}_{opt}", use_container_width=True):
                ok = (opt == m["correct"])
                done[str(idx)] = ok
                if ok:
                    st.success("✅ 這次答對了！")
                else:
                    st.error(f"❌ 正確答案：{m['correct']}")
                st.rerun()
    else:
        ok = done[str(idx)]
        if ok:
            st.markdown(f'<div class="fb-ok">✅ 答對！正確答案：{m["correct"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="fb-bad">❌ 答錯。正確答案：{m["correct"]}<br>你選了：{m["chosen"]}</div>', unsafe_allow_html=True)
        if st.button("下一題 →", type="primary"):
            S.rev_idx += 1; st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：單字庫
# ─────────────────────────────────────────────────────────────────────────────
def page_wordlist():
    st.markdown("## 📋 單字庫")

    cats = ["全部"] + sorted(set(w["cat"] for w in VOCAB))
    col1, col2 = st.columns([2, 1])
    with col1:
        query = st.text_input("🔍 搜尋單字或中文", value=S.wl_query, placeholder="allocate / 分配...")
    with col2:
        cat = st.selectbox("分類", cats)

    S.wl_query = query
    S.wl_cat = cat

    filtered = VOCAB
    if query:
        q = query.lower()
        filtered = [w for w in filtered if q in w["word"].lower() or q in w["zh"]]
    if cat != "全部":
        filtered = [w for w in filtered if w["cat"] == cat]

    st.markdown(f"<small style='color:#64748b'>顯示 {len(filtered)} / {len(VOCAB)} 筆</small>", unsafe_allow_html=True)
    st.markdown("---")

    for w in filtered:
        learned_mark = "✅ " if w["word"] in S.learned else ""
        st.markdown(f"""
        <div class="wl-row">
          <div class="wl-word">{learned_mark}{w['word']}</div>
          {tag_html(w['pos'])}
          <div class="wl-zh">{w['zh']}</div>
          <div class="wl-ex">{w['ex']}</div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 頁面：AI 出題
# ─────────────────────────────────────────────────────────────────────────────
def page_ai():
    st.markdown("## 🤖 AI 自動出題")
    st.info("從 120 個單字庫中隨機抽取，自動生成填空選擇題，快速鞏固單字記憶。")

    if st.button("🎲 生成 5 題", type="primary"):
        sample = random.sample(VOCAB, 5)
        qs = []
        TEMPLATES = [
            lambda w: f"The company decided to _____ the new policy. （{w['zh']}）",
            lambda w: f"She was praised for being highly _____ in her work. （{w['zh']}）",
            lambda w: f"We need to _____ our resources more effectively. （{w['zh']}）",
            lambda w: f"Please _____ the document before the meeting. （{w['zh']}）",
            lambda w: f"The manager asked the team to _____ the project. （{w['zh']}）",
        ]
        for i, w in enumerate(sample):
            same_pos = [x for x in VOCAB if x["pos"] == w["pos"] and x["word"] != w["word"]]
            wrongs = random.sample(same_pos, min(3, len(same_pos)))
            opts = [w["word"]] + [x["word"] for x in wrongs]
            random.shuffle(opts)
            qs.append({
                "q": TEMPLATES[i % len(TEMPLATES)](w),
                "opts": opts,
                "ans": opts.index(w["word"]),
                "exp": f"{w['word']}（{w['zh']}）— {w['ex']}"
            })
        st.session_state["ai_qs"] = qs
        st.session_state["ai_done"] = {}

    qs = st.session_state.get("ai_qs", [])
    ai_done = st.session_state.get("ai_done", {})

    for qi, q in enumerate(qs):
        st.markdown(f"**Q{qi+1}. {q['q']}**")
        answered = str(qi) in ai_done
        for i, opt in enumerate(q["opts"]):
            label = f"{chr(65+i)}. {opt}"
            if answered:
                if i == q["ans"]:
                    st.markdown(f'<div style="background:#ecfdf5;border:2px solid #10b981;border-radius:8px;padding:.5rem 1rem;margin:.2rem 0">✅ {label}</div>', unsafe_allow_html=True)
                elif i == ai_done[str(qi)]:
                    st.markdown(f'<div style="background:#fef2f2;border:2px solid #ef4444;border-radius:8px;padding:.5rem 1rem;margin:.2rem 0">❌ {label}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:.5rem 1rem;margin:.2rem 0;color:#94a3b8">{label}</div>', unsafe_allow_html=True)
            else:
                if st.button(label, key=f"ai_{qi}_{i}", use_container_width=True):
                    ai_done[str(qi)] = i
                    ok = (i == q["ans"])
                    S.correct += (1 if ok else 0); S.total += 1
                    if not ok:
                        add_mistake("vocab", q["q"], q["opts"][q["ans"]], opt)
                    st.session_state["ai_done"] = ai_done
                    st.rerun()
        if answered:
            st.markdown(f'<div class="fb-ok">💡 {q["exp"]}</div>', unsafe_allow_html=True)
        st.markdown("")

# ─────────────────────────────────────────────────────────────────────────────
# 主程式
# ─────────────────────────────────────────────────────────────────────────────
TABS = ["🏠 首頁", "📚 單字卡", "📝 文法", "🎧 聽力", "📖 閱讀", "⏱ 模擬考", "🔴 錯題", "📋 單字庫", "🤖 AI 出題"]
tabs = st.tabs(TABS)

with tabs[0]: page_home()
with tabs[1]: page_vocab()
with tabs[2]: page_grammar()
with tabs[3]: page_listening()
with tabs[4]: page_reading()
with tabs[5]: page_mock()
with tabs[6]: page_review()
with tabs[7]: page_wordlist()
with tabs[8]: page_ai()
