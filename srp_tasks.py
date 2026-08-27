# srp_tasks.py 
from abc import ABC, abstractmethod 

class TaskStorage(ABC): 
    @abstractmethod 
    def load_tasks(self): 
        pass
    @abstractmethod 
    def save_tasks(self, tasks): 
        pass

class FileTaskStorage(TaskStorage): 
    def __init__(self, filename="tasks.txt"): 
        self.filename = filename 

    def load_tasks(self): 
        loaded_tasks = [] 
        try: 
            with open(self.filename, "r") as f: 
                for line in f: 
                    parts = line.strip().split(',') 
                    if len(parts) >= 4: # ปรับเป็น >= 4 เพื่อรองรับไฟล์เก่า
                        task_id = int(parts[0]) 
                        description = parts[1] 
                        due_date = parts[2] if parts[2] != 'None' else None
                        completed = parts[3] == 'True'
                        # 3. ตรวจสอบว่ามีข้อมูล priority ในไฟล์ไหม ถ้าไม่มีให้ใช้ "Medium"
                        priority = parts[4] if len(parts) == 5 else "Medium"
                        
                        loaded_tasks.append(Task(task_id, description, due_date, completed, priority)) 
        except FileNotFoundError: 
            print(f"No existing task file '{self.filename}' found. Starting fresh.") 
        return loaded_tasks 

    def save_tasks(self, tasks): 
        with open(self.filename, "w") as f: 
            for task in tasks: 
                # 4. บันทึกข้อมูล priority ต่อท้าย
                f.write(f"{task.id},{task.description},{task.due_date},{task.completed},{task.priority}\n") 
        print(f"Tasks saved to {self.filename}")


class Task: 
    # 1. เพิ่ม parameter: priority (ตั้งค่าเริ่มต้นเป็น "Medium")
    def __init__(self, task_id, description, due_date=None, completed=False, priority="Medium"): 
        self.id = task_id 
        self.description = description 
        self.due_date = due_date 
        self.completed = completed
        self.priority = priority # เก็บค่า priority

    def mark_completed(self): 
        self.completed = True
        print(f"Task {self.id} '{self.description}' marked as completed.") 

    def __str__(self): 
        status = "✓" if self.completed else " "
        due = f" (Due: {self.due_date})" if self.due_date else ""
        # 2. ปรับการแสดงผลให้มี Priority ด้วย
        return f"[{status}] {self.id}. {self.description} [Priority: {self.priority}]{due}"

class TaskManager: 
    def __init__(self, storage: TaskStorage): 
        self.storage = storage 
        self.tasks = self.storage.load_tasks() 
        self.next_id = max([t.id for t in self.tasks] + [0]) + 1 if self.tasks else 1
        print(f"Loaded {len(self.tasks)} tasks. Next ID: {self.next_id}") 

    # 5. เพิ่ม priority มารับค่าที่ฟังก์ชัน
    def add_task(self, description, due_date=None, priority="Medium"): 
        # ส่ง priority เข้าไปตอนสร้าง Task
        task = Task(self.next_id, description, due_date, completed=False, priority=priority) 
        self.tasks.append(task) 
        self.next_id += 1
        self.storage.save_tasks(self.tasks) 
        print(f"Task '{description}' added with {priority} priority.") 
        return task

    def list_tasks(self): 
        print("\n--- Current Tasks ---") 
        if not self.tasks: 
            print("No tasks available.") 
            return
        for task in self.tasks: 
            print(task) 
        print("---------------------") 

    def get_task_by_id(self, task_id): 
        for task in self.tasks: 
            if task.id == task_id: 
                return task 
        return None

    def mark_task_completed(self, task_id): 
        task = self.get_task_by_id(task_id) 
        if task: 
            task.mark_completed() 
            self.storage.save_tasks(self.tasks) #Save after marking
            return True
        print(f"Task {task_id} not found.") 
        return False

if __name__ == "__main__": 
    file_storage = FileTaskStorage("my_tasks_v2.txt") 
    manager = TaskManager(file_storage) 

    # ลองใช้งานแบบใส่ priority
    manager.add_task("Review SOLID Principles", "2024-08-10", priority="High") 
    manager.add_task("Buy groceries", due_date=None, priority="Low") 
    
    manager.list_tasks()

print("Finished")