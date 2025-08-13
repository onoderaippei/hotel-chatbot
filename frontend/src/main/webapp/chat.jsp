<%@ page contentType="text/html; charset=UTF-8" %>
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>WAKON Concierge</title>
  <link rel="stylesheet" href="static/chat.css"/>
</head>
<body>
  <div class="wrap">
    <h2>WAKON Concierge (Local)</h2>
    <div class="ctrl">
      <label>言語:
        <select id="lang">
          <option value="ja" selected>日本語</option>
          <option value="en">English</option>
          <option value="zh">简体中文</option>
          <option value="ko">한국어</option>
        </select>
      </label>
      <button onclick="reloadFaq()">FAQリロード</button>
    </div>
    <div id="log" class="log"></div>
    <div class="input">
      <input id="q" autocomplete="off" placeholder="例：大浴場の営業時間は？ / 花束をお願い（部屋301）"/>
      <button onclick="send()">送信</button>
    </div>
  </div>
  <script>
  const API="http://localhost:8000";
  const logBox=document.getElementById('log');
  function log(html){ logBox.insertAdjacentHTML('beforeend', html); logBox.scrollTop=logBox.scrollHeight; }
  async function send(){
    const input=document.getElementById('q'); const q=input.value.trim();
    const lang=document.getElementById('lang').value; if(!q) return;
    log(`<div class='me'>👤 ${q}</div>`); input.value='';
    try{
      const res=await fetch(`${API}/api/chat/message`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:q,lang})});
      const data=await res.json(); render(data);
    }catch(e){ log(`<div class='bot err'>⚠️ 接続エラー: ${e}</div>`); }
  }
  function render(data){
    if(data.reply_type==='faq'){
      const th=data.payload.top_hit, alts=data.payload.alternatives||[];
      let html=`<div class='bot'><div class='card'><div class='title'>${th.title}</div><div class='ans'>${th.answer}</div><div class='cf'>信頼度: ${th.confidence}</div></div>`;
      if(alts.length){ html+=`<div class='alts'>他の候補：</div>`; alts.forEach(a=> html+=`<div class='alt'>・${a.title}（${a.confidence}）</div>`); }
      html+=`</div>`; log(html);
    }else if(data.reply_type==='ticket'){
      log(`<div class='bot'>📝 ご要望を受け付けました（ID: ${data.payload.ticket_id}）</div>`);
    }else{
      log(`<div class='bot'>🤖 ${data.payload.message||'…'}</div>`);
    }
  }
  async function reloadFaq(){ await fetch(`${API}/api/admin/reload`,{method:'POST'}); alert('FAQをリロードしました'); }
  document.getElementById('q').addEventListener('keydown',e=>{ if(e.key==='Enter') send(); });
  </script>
</body>
</html>
