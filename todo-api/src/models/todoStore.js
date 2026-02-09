class TodoStore {
  constructor() {
    this.todos = [];
    this.nextId = 1;
  }

  create(title) {
    const todo = {
      id: this.nextId++,
      title,
      completed: false
    };
    this.todos.push(todo);
    return todo;
  }

  findAll() {
    return this.todos;
  }

  findById(id) {
    return this.todos.find(todo => todo.id === id);
  }

  update(id, updates) {
    const todo = this.findById(id);
    if (!todo) return null;
    
    Object.assign(todo, updates);
    return todo;
  }

  delete(id) {
    const index = this.todos.findIndex(todo => todo.id === id);
    if (index === -1) return false;
    
    this.todos.splice(index, 1);
    return true;
  }

  clear() {
    this.todos = [];
    this.nextId = 1;
  }
}

export default new TodoStore();
