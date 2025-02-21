// HTML Templates
const authTemplate = `
    <div id="authForms">
        <div class="auth-toggle">
            <button onclick="auth.showLogin()">Login</button>
            <button onclick="auth.showRegister()">Register</button>
        </div>

        <form id="loginForm" class="auth-form">
            <h2>Login</h2>
            <input type="email" id="loginEmail" placeholder="Email" required>
            <input type="password" id="loginPassword" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>

        <form id="registerForm" class="auth-form hidden">
            <h2>Register</h2>
            <input type="email" id="registerEmail" placeholder="Email" required>
            <input type="password" id="registerPassword" placeholder="Password" required>
            <button type="submit">Register</button>
        </form>
    </div>
`;

const auth = {
  init() {
    if (!$('#authForms').length) {
      $('#app').append(authTemplate);
    }

    $('#loginForm').on('submit', (e) => {
      e.preventDefault();
      this.login();
    });

    $('#registerForm').on('submit', (e) => {
      e.preventDefault();
      this.register();
    });
  },

  showLogin() {
    $('#loginForm').removeClass('hidden');
    $('#registerForm').addClass('hidden');
  },

  showRegister() {
    $('#loginForm').addClass('hidden');
    $('#registerForm').removeClass('hidden');
  },

  login() {
    const username = $('#loginEmail').val();
    const password = $('#loginPassword').val();

    $.ajax({
        url: `${API_BASE_URL}/login`,
        method: 'POST',
        contentType: 'application/x-www-form-urlencoded',
        data: { username, password },
        success: (response) => {
            if (response.access_token) {  
                localStorage.setItem('token', response.access_token);  // ✅ Store token
                window.authToken = response.access_token;  // ✅ Global token
                console.log("Token Stored:", window.authToken);  // 🛠 Debugging Line
                app.showTodoApp();
            } else {
                alert('Login failed: No token received');
            }
        },
        error: (xhr) => {
            alert('Login failed: ' + (xhr.responseJSON?.detail || "Unknown error"));
        }
    });
},


  register() {
    const username = $('#registerEmail').val(); // Changed from email to username
    const password = $('#registerPassword').val();

    $.ajax({
      url: `${API_BASE_URL}/register`,
      method: 'POST',
      contentType: 'application/x-www-form-urlencoded', // Updated for FastAPI
      data: { username, password }, // Changed from JSON to form-urlencoded
      success: (response) => {
        alert('Registration successful! Please login.');
        this.showLogin();
      },
      error: (xhr) => {
        alert('Registration failed: ' + xhr.responseJSON.detail);
      }
    });
  },

  logout() {
    localStorage.removeItem('token');
    authToken = null;
    app.showAuthForms();
  }
};
