const express = require('express');
const Todo = require('../models/Todo');
const { authenticate } = require('../middleware/auth'); // Assuming you have an authentication middleware
const router = express.Router();

// Middleware to protect routes
router.use(authenticate);

// GET /todos
router.get('/', async (req, res) => {
    try {
        const todos = await Todo.find({ userId: req.user.id });
        res.status(200).json(todos);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// POST /todos
router.post('/', async (req, res) => {
    const { title } = req.body;
    try {
        const newTodo = new Todo({
            title,
            userId: req.user.id
        });
        await newTodo.save();
        res.status(201).json(newTodo);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

// PUT /todos/:id
router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const updates = req.body;
    try {
        const todo = await Todo.findOneAndUpdate({ _id: id, userId: req.user.id }, updates, { new: true });
        if (!todo) {
            return res.status(404).json({ message: 'Todo not found' });
        }
        res.status(200).json(todo);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

// DELETE /todos/:id
router.delete('/:id', async (req, res) => {
    const { id } = req.params;
    try {
        const todo = await Todo.findOneAndDelete({ _id: id, userId: req.user.id });
        if (!todo) {
            return res.status(404).json({ message: 'Todo not found' });
        }
        res.status(204).send();
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;