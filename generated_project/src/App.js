import React from 'react';
import AddTodo from './components/AddTodo';
import TodoList from './components/TodoList';
import { AuthProvider } from './context/AuthContext';
import './App.css';

const App = () => {
    return (
        <AuthProvider>
            <div>
                <h1>Todo List</h1>
                <AddTodo />
                <TodoList />
            </div>
        </AuthProvider>
    );
};

export default App;