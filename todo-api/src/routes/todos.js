import express from 'express';
import { createTodo, listTodos, getTodo, updateTodo, deleteTodo } from '../controllers/todoController.js';

const router = express.Router();

router.post('/', createTodo);
router.get('/', listTodos);
router.get('/:id', getTodo);
router.patch('/:id', updateTodo);
router.delete('/:id', deleteTodo);

export default router;
