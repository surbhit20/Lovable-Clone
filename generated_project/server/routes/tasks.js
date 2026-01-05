const express = require('express');
const router = express.Router();
const Task = require('../models/Task');
const mongoose = require('mongoose');

// Middleware to validate task ID
router.param('id', async (req, res, next, id) => {
  if (!mongoose.Types.ObjectId.isValid(id)) {
    return res.status(400).send('Invalid Task ID');
  }
  try {
    const task = await Task.findById(id);
    if (!task) {
      return res.status(404).send('Task not found');
    }
    req.task = task;
    next();
  } catch (error) {
    next(error);
  }
});

// POST /tasks - Create a new task
router.post('/tasks', async (req, res, next) => {
  try {
    const task = new Task(req.body);
    await task.save();
    res.status(201).send(task);
  } catch (error) {
    next(error);
  }
});

// GET /tasks - Retrieve all tasks
router.get('/tasks', async (req, res, next) => {
  try {
    const tasks = await Task.find({});
    res.send(tasks);
  } catch (error) {
    next(error);
  }
});

// PUT /tasks/:id - Update a task
router.put('/tasks/:id', async (req, res, next) => {
  try {
    const updatedTask = await Task.findByIdAndUpdate(req.params.id, req.body, { new: true });
    if (!updatedTask) {
      return res.status(404).send();
    }
    res.send(updatedTask);
  } catch (error) {
    next(error);
  }
});

// DELETE /tasks/:id - Delete a task
router.delete('/tasks/:id', async (req, res, next) => {
  try {
    const task = await Task.findByIdAndDelete(req.params.id);
    if (!task) {
      return res.status(404).send();
    }
    res.send(task);
  } catch (error) {
    next(error);
  }
});

// Error handling middleware
router.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

module.exports = router;