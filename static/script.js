async function loadTasks() {
    try {
        const res = await fetch("/tasks");
        const tasks = await res.json();

        const list = document.getElementById("taskList");
        const countSpan = document.getElementById("task-count");
        
        list.innerHTML = "";
        countSpan.textContent = tasks.length;

        tasks.forEach(task => {
            const li = document.createElement("li");

            // Create a wrapper for text to stack title over description
            li.innerHTML = `
                <div class="task-info">
                    <span class="task-title">${task.title}</span>
                    <span class="task-desc">${task.description || 'No description'}</span>
                </div>
                <button class="btn-delete">Delete</button>
            `;

            // Set up delete button logic
            const deleteBtn = li.querySelector(".btn-delete");
            deleteBtn.onclick = async () => {
                li.style.opacity = "0.5"; // Visual feedback
                await fetch(`/tasks/${task.id}`, { method: "DELETE" });
                loadTasks();
            };

            list.appendChild(li);
        });
    } catch (err) {
        console.error("Failed to load tasks:", err);
    }
}

async function addTask() {
    const titleInput = document.getElementById("title");
    const descInput = document.getElementById("description");

    if (!titleInput.value.trim()) {
        alert("Please enter a task title!");
        return;
    }

    const payload = { 
        title: titleInput.value, 
        description: descInput.value 
    };

    await fetch("/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    titleInput.value = "";
    descInput.value = "";
    loadTasks();
}

// Initial load
loadTasks();