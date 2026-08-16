import { getToken, showMessage } from "./api.js";

if (getToken()) window.location.href = "/records";

const loginForm = document.querySelector("#login-form");
const registerForm = document.querySelector("#register-form");

/** OAuth2のフォーム形式でログインし、返されたJWTを保存する。 */
loginForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new URLSearchParams({
    username: document.querySelector("#email").value,
    password: document.querySelector("#password").value,
  });

  try {
    const response = await fetch("/users/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData,
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "ログインに失敗しました。");
    sessionStorage.setItem("access_token", data.access_token);
    window.location.href = "/records";
  } catch (error) {
    showMessage(error.message);
  }
});

/** JSON形式でユーザーを登録し、ログイン画面へ案内する。 */
registerForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const body = {
    name: document.querySelector("#name").value,
    email: document.querySelector("#email").value,
    password: document.querySelector("#password").value,
  };
  try {
    const response = await fetch("/users/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "登録に失敗しました。");
    window.location.href = "/login";
  } catch (error) {
    showMessage(error.message);
  }
});
