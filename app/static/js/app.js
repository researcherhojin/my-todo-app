// Todo App - Frontend Logic

const API_URL = "/api/todos";

const todoForm = document.getElementById("todo-form");
const todoInput = document.getElementById("todo-input");
const todoList = document.getElementById("todo-list");
const emptyState = document.getElementById("empty-state");
const errorState = document.getElementById("error-state");
const listContainer = document.getElementById("todo-list-container");

let todos = [];

// --- API ---

async function fetchTodos() {
    listContainer.classList.add("loading");
    try {
        const res = await fetch(API_URL + "/");
        if (!res.ok) throw new Error("Failed to fetch");
        todos = await res.json();
        renderTodos();
        errorState.hidden = true;
    } catch {
        errorState.hidden = false;
        emptyState.hidden = true;
        todoList.innerHTML = "";
    } finally {
        listContainer.classList.remove("loading");
    }
}

async function addTodo(title) {
    const res = await fetch(API_URL + "/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title }),
    });
    if (!res.ok) throw new Error("Failed to add");
    const todo = await res.json();
    todos.push(todo);
    renderTodos();
}

async function toggleTodo(id, completed) {
    const res = await fetch(`${API_URL}/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ completed }),
    });
    if (!res.ok) throw new Error("Failed to toggle");
    const updated = await res.json();
    todos = todos.map((t) => (t.id === id ? updated : t));
    renderTodos();
}

async function deleteTodo(id) {
    const res = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Failed to delete");
    todos = todos.filter((t) => t.id !== id);
}

async function updateTodoTitle(id, title) {
    const res = await fetch(`${API_URL}/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title }),
    });
    if (!res.ok) throw new Error("Failed to update");
    const updated = await res.json();
    todos = todos.map((t) => (t.id === id ? updated : t));
    renderTodos();
}

// --- Render ---

function renderTodos() {
    todoList.innerHTML = "";

    if (todos.length === 0) {
        emptyState.hidden = false;
        return;
    }

    emptyState.hidden = true;

    todos.forEach((todo) => {
        const li = createTodoElement(todo);
        todoList.appendChild(li);
    });
}

function createTodoElement(todo) {
    const li = document.createElement("li");
    li.className = "todo-item" + (todo.completed ? " completed" : "");
    li.dataset.id = todo.id;

    // Checkbox
    const checkbox = document.createElement("div");
    checkbox.className = "todo-checkbox";
    checkbox.innerHTML = '<span class="todo-checkbox-mark">&#10003;</span>';
    checkbox.addEventListener("click", () => handleToggle(todo));

    // Title
    const title = document.createElement("span");
    title.className = "todo-title";
    title.textContent = todo.title;
    title.addEventListener("dblclick", () => startEditing(li, todo));

    // Delete
    const deleteBtn = document.createElement("button");
    deleteBtn.className = "todo-delete";
    deleteBtn.textContent = "\u00D7";
    deleteBtn.addEventListener("click", () => handleDelete(li, todo.id));

    li.appendChild(checkbox);
    li.appendChild(title);
    li.appendChild(deleteBtn);

    return li;
}

// --- Handlers ---

todoForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = todoInput.value.trim();
    if (!title) {
        todoInput.classList.add("shake");
        todoInput.addEventListener("animationend", () => todoInput.classList.remove("shake"), { once: true });
        return;
    }
    try {
        await addTodo(title);
        todoInput.value = "";
        todoInput.focus();
    } catch {
        // Silently handle — input stays for retry
    }
});

async function handleToggle(todo) {
    // Optimistic update
    const item = todoList.querySelector(`[data-id="${todo.id}"]`);
    if (item) item.classList.toggle("completed");

    try {
        await toggleTodo(todo.id, !todo.completed);
    } catch {
        // Rollback
        if (item) item.classList.toggle("completed");
    }
}

async function handleDelete(li, id) {
    // Set max-height before animating
    li.style.maxHeight = li.scrollHeight + "px";
    // Force reflow
    li.offsetHeight;
    li.classList.add("removing");

    try {
        await deleteTodo(id);
        li.addEventListener("transitionend", () => {
            li.remove();
            if (todos.length === 0) {
                emptyState.hidden = false;
            }
        }, { once: true });
    } catch {
        li.classList.remove("removing");
        li.style.maxHeight = "";
    }
}

function startEditing(li, todo) {
    if (todo.completed) return;

    const titleSpan = li.querySelector(".todo-title");
    const input = document.createElement("input");
    input.type = "text";
    input.className = "todo-edit-input";
    input.value = todo.title;

    titleSpan.replaceWith(input);
    input.focus();
    input.select();

    let saved = false;

    async function save() {
        if (saved) return;
        saved = true;
        const newTitle = input.value.trim();
        if (!newTitle || newTitle === todo.title) {
            // Revert
            const span = document.createElement("span");
            span.className = "todo-title";
            span.textContent = todo.title;
            span.addEventListener("dblclick", () => startEditing(li, todo));
            input.replaceWith(span);
            return;
        }
        try {
            await updateTodoTitle(todo.id, newTitle);
        } catch {
            // renderTodos will restore original
            renderTodos();
        }
    }

    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            save();
        }
        if (e.key === "Escape") {
            saved = true;
            const span = document.createElement("span");
            span.className = "todo-title";
            span.textContent = todo.title;
            span.addEventListener("dblclick", () => startEditing(li, todo));
            input.replaceWith(span);
        }
    });

    input.addEventListener("blur", save);
}

// --- Init ---
fetchTodos();
