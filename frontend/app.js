const sessionId = "s-" + Math.random().toString(36).slice(2, 10);
const messagesEl = document.getElementById("messages");
const suggEl = document.getElementById("suggestions");
const statusEl = document.getElementById("status");
const fmt = v => v.toLocaleString("vi-VN") + "đ";

function addMsg(text, who, meta, source) {
  const d = document.createElement("div");
  d.className = "msg " + who;
  d.textContent = text;
  if (meta) { const s = document.createElement("span"); s.className = "meta"; s.textContent = meta; d.appendChild(s); }
  if (source) { const s = document.createElement("span"); s.className = "source"; s.textContent = "Nguồn: " + source; d.appendChild(s); }
  messagesEl.appendChild(d);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function renderSuggestions(list) {
  suggEl.innerHTML = "";
  (list || []).forEach(q => {
    const b = document.createElement("button");
    b.type = "button"; b.textContent = q;
    b.onclick = () => send(q);
    suggEl.appendChild(b);
  });
}

async function send(text) {
  const msg = (text || document.getElementById("chatInput").value).trim();
  if (!msg) return;
  document.getElementById("chatInput").value = "";
  statusEl.textContent = "";
  addMsg(msg, "user");
  try {
    const r = await fetch("/chat", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg, session_id: sessionId }) });
    if (!r.ok) throw new Error("HTTP " + r.status);
    const data = await r.json();
    addMsg(data.reply, "bot",
      `intent: ${data.intent} · độ tin cậy: ${(data.confidence * 100).toFixed(0)}%${data.fallback ? " · fallback" : ""}`,
      data.source);
    renderSuggestions(data.suggestions);
  } catch (e) {
    statusEl.textContent = "Lỗi kết nối máy chủ: " + e.message;
  }
}

document.getElementById("chatForm").addEventListener("submit", e => { e.preventDefault(); send(); });

async function loadMajors() {
  try {
    const r = await fetch("/api/majors");
    const data = await r.json();
    const wrap = document.getElementById("majorList");
    data.majors.forEach(m => {
      const c = document.createElement("div");
      c.className = "card";
      c.innerHTML = `<h3></h3><p class="t"></p><p class="c"></p>`;
      c.querySelector("h3").textContent = m.name;
      c.querySelector(".t").textContent = "Học phí: " + fmt(m.tuition_per_year) + "/năm";
      c.querySelector(".c").textContent = "Tổ hợp: " + m.combos.join(", ");
      c.onclick = () => send("Học phí ngành " + m.name + " bao nhiêu?");
      wrap.appendChild(c);
    });
  } catch (e) { /* bo qua neu API loi */ }
}

addMsg("Chào bạn! Mình là trợ lý tuyển sinh ACU (dữ liệu minh họa). Bạn muốn hỏi về ngành học, học phí, điểm chuẩn hay gợi ý ngành theo sở thích?", "bot");
renderSuggestions(["Học phí ngành Công nghệ thông tin?", "Trường có những phương thức xét tuyển nào?", "Em thích lập trình, gợi ý ngành cho em", "Ký túc xá giá bao nhiêu?"]);
loadMajors();
