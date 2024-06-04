const TOKEN = "admin-demo-123"; // demo chi cho do an
const H = { "Content-Type": "application/json", "X-Admin-Token": TOKEN };

async function call(url, opts) {
  const r = await fetch(url, opts);
  const body = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(body.detail || ("HTTP " + r.status));
  return body;
}

document.getElementById("btnStats").onclick = async () => {
  const out = document.getElementById("statsOut");
  try {
    const s = await call("/api/admin/stats", { headers: H });
    let html = `<p>Tổng lượt hỏi: <strong>${s.total_user_messages}</strong></p>`;
    html += "<h3>Theo intent</h3><table><tr><th>Intent</th><th>Số câu</th></tr>" +
      Object.entries(s.by_intent).map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`).join("") + "</table>";
    html += "<h3>Câu hỏi chưa trả lời được (fallback)</h3>" +
      (s.fallback_questions.length
        ? "<ul>" + s.fallback_questions.map(q => `<li>${q.question} (${q.count} lần)</li>`).join("") + "</ul>"
        : "<p>Chưa có.</p>");
    html += "<h3>Câu hỏi thường gặp</h3><ul>" +
      s.top_questions.map(q => `<li>${q.question} (${q.count} lần)</li>`).join("") + "</ul>";
    out.innerHTML = html;
  } catch (e) { out.textContent = "Lỗi: " + e.message; }
};

document.getElementById("btnMajor").onclick = async () => {
  const msg = document.getElementById("majorMsg");
  try {
    const data = JSON.parse(document.getElementById("majorJson").value);
    await call("/api/admin/majors", { method: "POST", headers: H, body: JSON.stringify(data) });
    msg.textContent = "Đã lưu ngành. (Cần huấn luyện lại mô hình nếu đổi tên ngành để trích xuất entity tốt hơn.)";
  } catch (e) { msg.textContent = "Lỗi: " + e.message; }
};

document.getElementById("btnDelMajor").onclick = async () => {
  const msg = document.getElementById("majorMsg");
  try {
    const code = document.getElementById("delMajorCode").value.trim();
    await call("/api/admin/majors/" + encodeURIComponent(code), { method: "DELETE", headers: H });
    msg.textContent = "Đã xóa ngành " + code;
  } catch (e) { msg.textContent = "Lỗi: " + e.message; }
};

document.getElementById("btnFaq").onclick = async () => {
  const msg = document.getElementById("faqMsg");
  try {
    const data = JSON.parse(document.getElementById("faqJson").value);
    await call("/api/admin/faqs", { method: "POST", headers: H, body: JSON.stringify(data) });
    msg.textContent = "Đã lưu FAQ.";
  } catch (e) { msg.textContent = "Lỗi: " + e.message; }
};

document.getElementById("btnDelFaq").onclick = async () => {
  const msg = document.getElementById("faqMsg");
  try {
    const id = document.getElementById("delFaqId").value.trim();
    await call("/api/admin/faqs/" + encodeURIComponent(id), { method: "DELETE", headers: H });
    msg.textContent = "Đã xóa FAQ " + id;
  } catch (e) { msg.textContent = "Lỗi: " + e.message; }
};
