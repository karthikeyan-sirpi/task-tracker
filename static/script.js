async function loadTasks() {
    const res = await fetch("/tasks");
    const tasks = await res.json();

    const list = document.getElementById("taskList");
    list.innerHTML = "";

    tasks.forEach(task => {
        const li = document.createElement("li");
        li.textContent = task.title + " - " + task.description;

        const btn = document.createElement("button");
        btn.textContent = "Delete";
        btn.onclick = async () => {
            await fetch(`/tasks/${task.id}`, { method: "DELETE" });
            loadTasks();
        };

        li.appendChild(btn);
        list.appendChild(li);
    });
}

async function addTask() {
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;

    await fetch("/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, description })
    });

    document.getElementById("title").value = "";
    document.getElementById("description").value = "";

    loadTasks();
}

loadTasks();