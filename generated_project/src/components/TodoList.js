import React, { useEffect, useState } from 'react';
import TodoItem from './TodoItem';
import { getTodos } from '../services/todoService';

const TodoList = ({ onEdit }) => {
    const [todos, setTodos] = useState([]);
    const [filter, setFilter] = useState('all');

    useEffect(() => {
        const fetchTodos = async () => {
            const fetchedTodos = await getTodos();
            setTodos(fetchedTodos);
        };
        fetchTodos();
    }, []);

    const filteredTodos = todos.filter(todo => {
        if (filter === 'active') return !todo.completed;
        if (filter === 'completed') return todo.completed;
        return true; // 'all'
    });

    return (
        <div className="todo-list">
            <div className="filter-buttons">
                <button onClick={() => setFilter('all')}>All</button>
                <button onClick={() => setFilter('active')}>Active</button>
                <button onClick={() => setFilter('completed')}>Completed</button>
            </div>
            {filteredTodos.map(todo => (
                <TodoItem key={todo.id} todo={todo} onEdit={onEdit} />
            ))}
        </div>
    );
};

export default TodoList;