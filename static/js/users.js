import { apiFetch, readJson, requireLogin, setupLogoutButton, showMessage, logout } from "./api.js";

if (requireLogin()) {
  setupLogoutButton();
  loadUser();
  document.querySelector("#user-form").addEventListener("submit", updateUser);
  document.querySelector("#delete-user").addEventListener("click", deleteUser);
}

/** ログイン中ユーザーのプロフィールをフォームへ読み込む。 */
async function loadUser() {
  try {
    const user = await apiFetch("/users/").then(readJson);
    document.querySelector("#name").value = user.name;
    document.querySelector("#email").value = user.email;
  } catch (error) { showMessage(error.message); }
}

/** プロフィールの名前とメールアドレスを更新する。 */
async function updateUser(event) {
  event.preventDefault();
  const body = { name: document.querySelector("#name").value, email: document.querySelector("#email").value };
  try {
    const response = await apiFetch("/users/", { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    const data = await readJson(response);
    showMessage(data.message, false);
  } catch (error) { showMessage(error.message); }
}

/** 確認後にログイン中ユーザーを削除する。 */
async function deleteUser() {
  if (!window.confirm("アカウントを削除しますか？この操作は元に戻せません。")) return;
  try {
    await apiFetch("/users/", { method: "DELETE" }).then(readJson);
    logout();
  } catch (error) { showMessage(error.message); }
}
