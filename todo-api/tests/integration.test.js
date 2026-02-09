const request = require('supertest');
const app = require('../src/app');
const todoStore = require('../src/models/todoStore');

describe('Todo API Integration Tests', () => {
  beforeEach(() => {
    todoStore.clear();
  });

  describe('Complete API Flow', () => {
    it('should execute full CRUD sequence', async () => {
      // 1. Create a todo
      const createRes = await request(app)
        .post('/todos')
        .send({ title: 'Buy groceries' })
        .expect(201);

      expect(createRes.body).toMatchObject({
        id: expect.any(Number),
        title: 'Buy groceries',
        completed: false
      });

      const todoId = createRes.body.id;

      // 2. List todos
      const listRes = await request(app)
        .get('/todos')
        .expect(200);

      expect(listRes.body).toHaveLength(1);
      expect(listRes.body[0]).toMatchObject({
        id: todoId,
        title: 'Buy groceries',
        completed: false
      });

      // 3. Get todo by ID
      const getRes = await request(app)
        .get(`/todos/${todoId}`)
        .expect(200);

      expect(getRes.body).toMatchObject({
        id: todoId,
        title: 'Buy groceries',
        completed: false
      });

      // 4. Update todo (mark as completed)
      const patchRes = await request(app)
        .patch(`/todos/${todoId}`)
        .send({ completed: true })
        .expect(200);

      expect(patchRes.body).toMatchObject({
        id: todoId,
        title: 'Buy groceries',
        completed: true
      });

      // 5. Verify the update
      const verifyRes = await request(app)
        .get(`/todos/${todoId}`)
        .expect(200);

      expect(verifyRes.body.completed).toBe(true);

      // 6. Delete todo
      await request(app)
        .delete(`/todos/${todoId}`)
        .expect(204);

      // 7. Verify deletion
      await request(app)
        .get(`/todos/${todoId}`)
        .expect(404);

      // 8. Verify list is empty
      const finalListRes = await request(app)
        .get('/todos')
        .expect(200);

      expect(finalListRes.body).toHaveLength(0);
    });
  });

  describe('POST /todos', () => {
    it('should create a new todo with valid title', async () => {
      const res = await request(app)
        .post('/todos')
        .send({ title: 'Test todo' })
        .expect(201);

      expect(res.body).toMatchObject({
        id: expect.any(Number),
        title: 'Test todo',
        completed: false
      });
    });

    it('should reject todo without title', async () => {
      await request(app)
        .post('/todos')
        .send({})
        .expect(400);
    });

    it('should reject todo with empty title', async () => {
      await request(app)
        .post('/todos')
        .send({ title: '   ' })
        .expect(400);
    });

    it('should reject todo with non-string title', async () => {
      await request(app)
        .post('/todos')
        .send({ title: 123 })
        .expect(400);
    });
  });

  describe('GET /todos', () => {
    it('should return empty array initially', async () => {
      const res = await request(app)
        .get('/todos')
        .expect(200);

      expect(res.body).toEqual([]);
    });

    it('should return all todos', async () => {
      await request(app).post('/todos').send({ title: 'Todo 1' });
      await request(app).post('/todos').send({ title: 'Todo 2' });

      const res = await request(app)
        .get('/todos')
        .expect(200);

      expect(res.body).toHaveLength(2);
      expect(res.body[0].title).toBe('Todo 1');
      expect(res.body[1].title).toBe('Todo 2');
    });
  });

  describe('GET /todos/:id', () => {
    it('should return a specific todo', async () => {
      const createRes = await request(app)
        .post('/todos')
        .send({ title: 'Specific todo' });

      const todoId = createRes.body.id;

      const res = await request(app)
        .get(`/todos/${todoId}`)
        .expect(200);

      expect(res.body).toMatchObject({
        id: todoId,
        title: 'Specific todo',
        completed: false
      });
    });

    it('should return 404 for non-existent todo', async () => {
      await request(app)
        .get('/todos/999')
        .expect(404);
    });

    it('should return 400 for invalid ID format', async () => {
      await request(app)
        .get('/todos/abc')
        .expect(400);
    });
  });

  describe('PATCH /todos/:id', () => {
    it('should update todo completion status', async () => {
      const createRes = await request(app)
        .post('/todos')
        .send({ title: 'Update test' });

      const todoId = createRes.body.id;

      const res = await request(app)
        .patch(`/todos/${todoId}`)
        .send({ completed: true })
        .expect(200);

      expect(res.body.completed).toBe(true);
      expect(res.body.title).toBe('Update test');
    });

    it('should update todo title', async () => {
      const createRes = await request(app)
        .post('/todos')
        .send({ title: 'Original title' });

      const todoId = createRes.body.id;

      const res = await request(app)
        .patch(`/todos/${todoId}`)
        .send({ title: 'Updated title' })
        .expect(200);

      expect(res.body.title).toBe('Updated title');
    });

    it('should update both title and completion', async () => {
      const createRes = await request(app)
        .post('/todos')
        .send({ title: 'Original' });

      const todoId = createRes.body.id;

      const res = await request(app)
        .patch(`/todos/${todoId}`)
        .send({ title: 'Updated', completed: true })
        .expect(200);

      expect(res.body.title).toBe('Updated');
      expect(res.body.completed).toBe(true);
    });

    it('should return 404 for non-existent todo', async () => {
      await request(app)
        .patch('/todos/999')
        .send({ completed: true })
        .expect(404);
    });

    it('should reject invalid completed value', async () => {
      const createRes = await request(app)
        .post('/todos')
        .send({ title: 'Test' });

      const todoId = createRes.body.id;

      await request(app)
        .patch(`/todos/${todoId}`)
        .send({ completed: 'yes' })
        .expect(400);
    });

    it('should reject empty title', async () => {
      const createRes = await request(app)
        .post('/todos')
        .send({ title: 'Test' });

      const todoId = createRes.body.id;

      await request(app)
        .patch(`/todos/${todoId}`)
        .send({ title: '   ' })
        .expect(400);
    });
  });

  describe('DELETE /todos/:id', () => {
    it('should delete a todo', async () => {
      const createRes = await request(app)
        .post('/todos')
        .send({ title: 'To be deleted' });

      const todoId = createRes.body.id;

      await request(app)
        .delete(`/todos/${todoId}`)
        .expect(204);

      await request(app)
        .get(`/todos/${todoId}`)
        .expect(404);
    });

    it('should return 404 when deleting non-existent todo', async () => {
      await request(app)
        .delete('/todos/999')
        .expect(404);
    });

    it('should return 400 for invalid ID format', async () => {
      await request(app)
        .delete('/todos/abc')
        .expect(400);
    });
  });
});
