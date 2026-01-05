import React, { useState, useEffect } from 'react';
import { editTodo } from '../services/todoService';

const EditTodo = ({ currentTask, onUpdate }) => {
    const [task, setTask] = useState('');

    useEffect(() => {
        if (currentTask) {
            setTask(currentTask.text);
        }
    }, [currentTask]);

    const handleChange = (e) => {
        setTask(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (currentTask) {
            editTodo(currentTask.id, { text: task })
                .then(() => {
                    onUpdate(); // Callback to refresh the task list
                })
                .catch((error) => {
                    console.error('Error editing task:', error);
                });
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" value={task} onChange={handleChange} required />
            <button type="submit">Edit Task</button>
        </form>
    );
};

export default EditTodo;