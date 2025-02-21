// HTML Templates
const todoTemplate = `
    <div id="todoApp" class="hidden">
        <h1>My Todo List</h1>
        <div class="add-todo">
            <input type="text" id="newTodoTitle" placeholder="Enter Task Title">
            <textarea id="newTodoDescription" placeholder="Enter Task Description"></textarea>
            <button onclick="todos.create()">Add</button>
        </div>
        <div id="todoList"></div>
        <button onclick="auth.logout()" class="logout-btn">Logout</button>
    </div>
`;

const todos = {
    init() {
        if (!$('#todoApp').length) {
            $('#app').append(todoTemplate);
        }
        this.load();
    },

    load() {
        let authToken = localStorage.getItem('token');
        console.log("🟢 Sending Token in Header:", authToken);

        if (!authToken) {
            alert("Session expired! Please login again.");
            auth.logout();
            return;
        }

        $.ajax({
            url: `${API_BASE_URL}/user/todos`,
            method: 'GET',
            headers: { 'Authorization': `Bearer ${authToken}` },
            success: (todos) => {
                console.log("✅ Todos Loaded:", todos);
                this.display(todos);
            },
            error: (xhr) => {
                console.error("❌ Error Response:", xhr.responseText);
                if (xhr.status === 401) {
                    alert("Unauthorized! Logging out...");
                    auth.logout();
                } else {
                    alert('Failed to load todos: ' + xhr.responseText);
                }
            }
        });
    },

    create() {
        let authToken = localStorage.getItem('token');
        console.log("🟢 Sending Token in Header:", authToken);

        let title = $('#newTodoTitle').val().trim();
        let description = $('#newTodoDescription').val().trim();

        console.log("🔍 Title:", title);
        console.log("🔍 Description:", description);

        if (!title || !description) {
            alert("Please enter both title and description!");
            return;
        }

        $.ajax({
            url: `${API_BASE_URL}/todos`,
            method: 'POST',
            contentType: 'application/json',
            headers: { 'Authorization': `Bearer ${authToken}` },
            data: JSON.stringify({ title, description }),
            success: (response) => {
                console.log("✅ Task Created:", response);
                $('#newTodoTitle').val('');
                $('#newTodoDescription').val('');
                this.load();
            },
            error: (xhr) => {
                console.error("❌ Error Response:", xhr.responseText);
                if (xhr.status === 401) {
                    alert("Unauthorized! Please login again.");
                    auth.logout();
                } else {
                    alert('Failed to create task: ' + xhr.responseText);
                }
            }
        });
    },

    update(id, updates) {
        let authToken = localStorage.getItem('token');
        $.ajax({
            url: `${API_BASE_URL}/todos/update/${id}`,
            method: 'PUT',
            contentType: 'application/json',
            headers: { 'Authorization': `Bearer ${authToken}` },
            data: JSON.stringify(updates),
            success: (response) => {
                console.log("✅ Todo Updated:", response);
                this.load();
            },
            error: (xhr) => {
                alert('Failed to update todo: ' + xhr.responseText);
            }
        });
    },

    delete(id) {
        let authToken = localStorage.getItem('token');
        if (!confirm('Are you sure you want to delete this todo?')) return;

        $.ajax({
            url: `${API_BASE_URL}/todos/delete/${id}`,
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken}` },
            success: () => {
                console.log(`✅ Todo ${id} deleted successfully`);
                this.load();
            },
            error: (xhr) => {
                alert('Failed to delete todo: ' + xhr.responseText);
            }
        });
    },

    toggleComplete(id, completed) {
        this.update(id, { is_complete: !completed });
    },

    edit(id) {
        const todoItem = $(`#todo-${id}`);
        const oldTitle = todoItem.find('.text').text();
        const oldDescription = todoItem.find('.description').text(); // ✅ Get old description

        // Ask user for new title and description
        const newTitle = prompt('Edit todo title:', oldTitle);
        const newDescription = prompt('Edit todo description:', oldDescription);

        // If user didn't cancel and made valid changes
        if (newTitle !== null && newDescription !== null &&
            newTitle.trim() !== '' && newDescription.trim() !== '' &&
            (newTitle !== oldTitle || newDescription !== oldDescription)) {

            this.update(id, { title: newTitle, description: newDescription }); // ✅ Send both updates
        }
    },

    display(todoList) {
        const todoListElement = $('#todoList');
        todoListElement.empty();

        todoList.forEach(todo => {
            const todoElement = $(`
                <div id="todo-${todo.id}" class="todo-item ${todo.is_complete ? 'completed' : ''}">  
                    <span class="text">${todo.title}</span>
                    <p class="description">${todo.description}</p>
                    <span class="priority ${todo.priority.toLowerCase()}">Priority: ${todo.priority}</span>
                    <div class="todo-actions">
                        <button class="complete-btn" onclick="todos.toggleComplete(${todo.id}, ${todo.is_complete})">
                            ${todo.is_complete ? 'Undo' : 'Complete'}
                        </button>
                        <button class="edit-btn" onclick="todos.edit(${todo.id})">Edit</button>
                        <button class="delete-btn" onclick="todos.delete(${todo.id})">Delete</button>
                    </div>
                </div>
            `);
            todoListElement.append(todoElement);
        });
    }
};
