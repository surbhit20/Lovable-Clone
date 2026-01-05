import React from 'react';
import { deleteTodo } from '../services/todoService';

const TodoItem = ({ todo, onEdit }) => {
    const handleDelete = async () => {
        try {
            await deleteTodo(todo.id);
            // Optionally, you can call a function to refresh the list or update the state
        } catch (error) {
            console.error('Failed to delete todo:', error);
        }
    };

    return (
        <div className="todo-item">
            <h3>{todo.title}</h3>
            <button onClick={() => onEdit(todo)}>Edit</button>
            <button onClick={handleDelete}>Delete</button>
        </div>
    );
};

export default TodoItem;