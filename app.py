from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json

app = Flask(__name__)

# Fungsi untuk memuat tugas dari file JSON
def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            tasks_data = json.load(file)
            # Mengonversi string deadline kembali ke objek datetime
            for task in tasks_data:
                task["deadline"] = datetime.fromisoformat(task["deadline"])
            return tasks_data
    except FileNotFoundError:
        return []

# Fungsi untuk menyimpan tugas ke dalam file JSON
def save_tasks():
    # Mengonversi datetime ke string format ISO
    tasks_to_save = [
        {
            "name": task["name"],
            "deadline": task["deadline"].isoformat(),  # Mengonversi datetime menjadi string
            "status": task["status"]
        }
        for task in tasks
    ]
    
    with open("tasks.json", "w") as file:
        json.dump(tasks_to_save, file)

# Inisialisasi tugas dengan memuat data dari file JSON
tasks = load_tasks()

@app.route("/", methods=["GET", "POST"])
def task():
    if request.method == "POST":
        task_name = request.form["task_name"]
        deadline = request.form["deadline"]
        deadline = datetime.fromisoformat(deadline)
        tasks.append({"name": task_name, "deadline": deadline, "status": "Not Finished"})
        
        save_tasks()  # Simpan tugas yang baru ditambahkan
        return redirect(url_for("task"))

    return render_template("index.html", tasks=tasks)

@app.route("/update_status/<int:task_index>", methods=["POST"])
def update_status(task_index):
    task = tasks[task_index]
    # Toggle status antara "Finished" dan "Not Finished"
    task['status'] = "Finished" if task['status'] == "Not Finished" else "Not Finished"
    save_tasks()
    return redirect(url_for("task"))

@app.route("/delete_task/<int:task_index>")
def delete_task(task_index):
    # Hapus tugas yang sudah selesai
    del tasks[task_index]
    save_tasks()
    return redirect(url_for("task"))

@app.after_request
def save_task_data(response):
    save_tasks()  # Simpan tugas setelah setiap request
    return response

if __name__ == "__main__":
    app.run(debug=True)
