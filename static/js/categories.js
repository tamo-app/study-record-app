import { apiFetch, readJson, requireLogin, setupLogoutButton, showMessage } from "./api.js";

if (requireLogin()) {
  setupLogoutButton();
  if (document.querySelector("#categories")) loadCategories();
  if (document.querySelector("#category-form")) setupCategoryForm();
}

/** カテゴリ一覧を取得して、編集・削除ボタンとともに表示する。 */
async function loadCategories() {
  try {
    const data = await apiFetch("/categories/").then(readJson);
    const container = document.querySelector("#categories");
    container.replaceChildren();
    if (data.categories.length === 0) container.textContent = "カテゴリはまだありません。";
    data.categories.forEach((category) => container.append(createCategoryItem(category)));
  } catch (error) { showMessage(error.message); }
}

/** カテゴリ1件の表示要素を作る。 */
function createCategoryItem(category) {
  const article = document.createElement("article");
  article.className = "list-item";
  const title = document.createElement("h2"); title.textContent = category.name;
  const detail = document.createElement("p"); detail.textContent = category.detail || "詳細はありません。";
  const edit = document.createElement("a"); edit.className = "button secondary"; edit.href = `/category-form?id=${category.id}`; edit.textContent = "編集";
  const remove = document.createElement("button"); remove.className = "danger"; remove.textContent = "削除";
  remove.addEventListener("click", () => deleteCategory(category.id));
  article.append(title, detail, edit, remove);
  return article;
}

/** 編集時は一覧から対象カテゴリの値を読み込み、フォームに設定する。 */
async function setupCategoryForm() {
  const id = new URLSearchParams(window.location.search).get("id");
  if (id) {
    try {
      const data = await apiFetch("/categories/").then(readJson);
      const category = data.categories.find((item) => item.id === Number(id));
      if (!category) return showMessage("カテゴリが見つかりません。");
      document.querySelector("#form-title").textContent = "カテゴリを編集";
      document.querySelector("#name").value = category.name;
      document.querySelector("#detail").value = category.detail || "";
    } catch (error) { showMessage(error.message); return; }
  }

  document.querySelector("#category-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const body = { name: document.querySelector("#name").value, detail: document.querySelector("#detail").value };
    try {
      const response = await apiFetch(id ? `/categories/${id}` : "/categories/", { method: id ? "PUT" : "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      await readJson(response);
      window.location.href = "/categories";
    } catch (error) { showMessage(error.message); }
  });
}

/** カテゴリ削除を実行し、409の場合は理由を分かりやすく表示する。 */
async function deleteCategory(id) {
  if (!window.confirm("このカテゴリを削除しますか？")) return;
  try {
    await apiFetch(`/categories/${id}`, { method: "DELETE" }).then(readJson);
    loadCategories();
  } catch (error) {
    if (error.status === 409) showMessage("このカテゴリには学習記録があるため削除できません。");
    else if (error.status === 404) showMessage("カテゴリが見つかりません。");
    else showMessage(error.message);
  }
}
