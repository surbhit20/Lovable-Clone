import axios from 'axios';

const API_URL = '/todos';

export const getTodos = async () => {
    try {
        const response = await axios.get(API_URL);
        return response.data;
    } catch (error) {
        throw new Error('Error fetching todos: ' + error.message);
    }
};

export const addTodo = async (title) => {
    try {
        const response = await axios.post(API_URL, { title });
        return response.data;
    } catch (error) {
        throw new Error('Error adding todo: ' + error.message);
    }
};

export const editTodo = async (id, updates) => {
    try {
        const response = await axios.put(`${API_URL}/${id}`, updates);
        return response.data;
    } catch (error) {
        throw new Error('Error editing todo: ' + error.message);
    }
};

export const deleteTodo = async (id) => {
    try {
        await axios.delete(`${API_URL}/${id}`);
    } catch (error) {
        throw new Error('Error deleting todo: ' + error.message);
    }
};
