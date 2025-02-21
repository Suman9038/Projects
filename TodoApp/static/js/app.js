const app = {
    init() {
        auth.init();
        const authToken = localStorage.getItem('token');
        
        if (authToken) {
            this.checkAuth(authToken);  // Check token by fetching todos
        } else {
            this.showAuthForms();
        }
    },

    checkAuth(token) {
        $.ajax({
            url: `${API_BASE_URL}/todos`,  // Try fetching todos
            method: 'GET',
            headers: { Authorization: `Bearer ${token}` },
            success: () => {
                this.showTodoApp();
            },
            error: (xhr) => {
                if (xhr.status === 401) { // If token is invalid, log out
                    auth.logout();
                }
            }
        });
    },

    showAuthForms() {
        $('#authForms').removeClass('hidden');
        $('#todoApp').addClass('hidden');
    },

    showTodoApp() {
        $('#authForms').addClass('hidden');
        $('#todoApp').removeClass('hidden');
        todos.init();
    }
};

// Initialize the app when document is ready
$(document).ready(() => {
    app.init();
});
