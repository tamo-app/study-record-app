const TOKEN_KEY = "access_token";

/** JWTを取得する。 */
export function getToken() {
  return sessionStorage.getItem(TOKEN_KEY);
}

/** JWTを削除してログイン画面へ戻る。 */
export function logout() {
  sessionStorage.removeItem(TOKEN_KEY);
  window.location.href = "/login";
}

/** ログインしていない利用者をログイン画面へ案内する。 */
export function requireLogin() {
  if (!getToken()) {
    window.location.href = "/login";
    return false;
  }
  return true;
}

/** 認証ヘッダーを付けてJSON APIを呼び出す。401の場合はログアウトする。 */
export async function apiFetch(url, options = {}) {
  const headers = new Headers(options.headers || {});
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const response = await fetch(url, { ...options, headers });
  if (response.status === 401) {
    logout();
    throw new Error("ログインの有効期限が切れました。");
  }
  return response;
}

/** APIレスポンスを読み込み、失敗時にはHTTPステータスも保持したエラーを返す。 */
export async function readJson(response) {
  let data = {};
  try {
    data = await response.json();
  } catch {
    // JSONでないエラー応答でも、画面側でエラーメッセージを表示できるようにする。
  }
  if (!response.ok) {
    const error = new Error(data.detail || `処理に失敗しました。（HTTP ${response.status}）`);
    error.status = response.status;
    throw error;
  }
  return data;
}

/** 画面上のメッセージ領域に結果を表示する。 */
export function showMessage(text, isError = true) {
  const element = document.querySelector("#message");
  if (!element) return;
  element.textContent = text;
  element.className = isError ? "message error" : "message success";
}

/** すべての画面にあるログアウトボタンを有効化する。 */
export function setupLogoutButton() {
  document.querySelector("[data-logout]")?.addEventListener("click", logout);
}
