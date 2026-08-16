import { apiFetch, readJson, requireLogin, setupLogoutButton, showMessage } from "./api.js";

if (requireLogin()) {
  setupLogoutButton();
  if (document.querySelector("#records")) loadRecordsPage();
  if (document.querySelector("#record-detail")) loadRecordDetail();
  if (document.querySelector("#record-form")) setupRecordForm();
}

/** 記録一覧とカテゴリ別合計を取得して表示する。 */
async function loadRecordsPage() {
  try {
    const [recordsData, summaryData] = await Promise.all([
      apiFetch("/records/").then(readJson),
      apiFetch("/records/summary/").then(readJson),
    ]);
    const recordsElement = document.querySelector("#records");
    const summaryElement = document.querySelector("#summary");
    recordsElement.replaceChildren();
    summaryElement.replaceChildren();

    if (recordsData.records.length === 0) recordsElement.textContent = "学習記録はまだありません。";
    recordsData.records.forEach((record) => recordsElement.append(createRecordItem(record)));
    if (summaryData.summary.length === 0) summaryElement.textContent = "集計できる学習記録はまだありません。";
    summaryData.summary.forEach((item) => {
      const card = document.createElement("div");
      card.className = "summary-card";
      card.textContent = `${item.category_name}: ${item.study_minutes}分`;
      summaryElement.append(card);
    });
  } catch (error) { showMessage(error.message); }
}

/** 一覧に表示する記録1件の要素を作る。 */
function createRecordItem(record) {
  const article = document.createElement("article");
  article.className = "list-item";
  const link = document.createElement("a");
  link.href = `/record-detail?id=${record.id}`;
  link.textContent = record.title;
  const text = document.createElement("p");
  text.textContent = `${record.category_name} / ${record.study_minutes}分`;
  article.append(link, text);
  return article;
}

/** URLのidを使って記録詳細を取得して表示する。 */
async function loadRecordDetail() {
  const id = new URLSearchParams(window.location.search).get("id");
  if (!id) return showMessage("表示する記録が指定されていません。");
  try {
    const data = await apiFetch(`/records/${id}`).then(readJson);
    const record = data.record;
    const article = document.querySelector("#record-detail");
    article.replaceChildren();
    const title = document.createElement("h1"); title.textContent = record.title;
    const meta = document.createElement("p"); meta.textContent = `${record.category_name} / ${record.study_minutes}分`;
    const detail = document.createElement("p"); detail.textContent = record.detail || "詳細はありません。";
    const edit = document.createElement("a"); edit.className = "button"; edit.href = `/record-form?id=${record.id}`; edit.textContent = "編集する";
    const remove = document.createElement("button"); remove.className = "danger"; remove.textContent = "削除する";
    remove.addEventListener("click", () => deleteRecord(record.id));
    article.append(title, meta, detail, edit, remove);
  } catch (error) { showMessage(error.status === 404 ? "学習記録が見つかりません。" : error.message); }
}

/** カテゴリ選択肢を取得し、編集時は既存値もフォームに設定する。 */
async function setupRecordForm() {
  const id = new URLSearchParams(window.location.search).get("id");
  try {
    const categoryData = await apiFetch("/categories/").then(readJson);
    const select = document.querySelector("#category-id");
    select.replaceChildren(new Option("カテゴリを選択", ""));
    categoryData.categories.forEach((category) => select.add(new Option(category.name, category.id)));
    if (id) {
      document.querySelector("#form-title").textContent = "学習記録を編集";
      const data = await apiFetch(`/records/${id}`).then(readJson);
      const record = data.record;
      document.querySelector("#title").value = record.title;
      document.querySelector("#study-minutes").value = record.study_minutes;
      document.querySelector("#detail").value = record.detail || "";
      const category = categoryData.categories.find((item) => item.name === record.category_name);
      if (category) select.value = category.id;
    }
  } catch (error) { showMessage(error.message); return; }

  document.querySelector("#record-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const body = { category_id: Number(document.querySelector("#category-id").value), title: document.querySelector("#title").value, study_minutes: Number(document.querySelector("#study-minutes").value), detail: document.querySelector("#detail").value };
    try {
      const response = await apiFetch(id ? `/records/${id}` : "/records/", { method: id ? "PUT" : "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      await readJson(response);
      window.location.href = id ? `/record-detail?id=${id}` : "/records";
    } catch (error) { showMessage(error.message); }
  });
}

/** 確認後に記録を削除する。 */
async function deleteRecord(id) {
  if (!window.confirm("この学習記録を削除しますか？")) return;
  try {
    await apiFetch(`/records/${id}`, { method: "DELETE" }).then(readJson);
    window.location.href = "/records";
  } catch (error) { showMessage(error.message); }
}
