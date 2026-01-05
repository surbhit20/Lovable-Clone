import React, { useState } from 'react';
import { addTodo } from '../services/todoService';

const AddTodo = () => {
    const [title, setTitle] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!title) return;

        try {
            await addTodo(title);
            setTitle(''); // Clear the input field after submission
        } catch (error) {
            console.error('Failed to add todo:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter task title"
                required
            />
            <button type="submit">Add Todo</button>
        </form>
    );
};

export default AddTodo;