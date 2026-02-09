import express from 'express';
import todoRoutes from './routes/todos.js';
const app = express(); 
app.use(express.json()); 
app.use('/todos', todoRoutes); 
// Health check endpoint 
app.get('/health', (req, res) => { 
res.json({ status: 'ok' }); }); 
// 404 handler 
app.use((req, res) => { 
res.status(404).json({ error: 'Not found' });
});
 // Error handler 
 app.use((err, req, res, next) => {
console.error(err.stack); 
res.status(500).json({ 
error: 'Internal server error' }); 
});
export default app;
