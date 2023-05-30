
import React, { useState, useEffect } from 'react';
import './App.css';
import TodoListView from './TodoListView/TodoListView';
import TrashBinView from './TrashBinView/TrashBinView';
import axios from 'axios';

function App() {
    const [todoList, setTodoList] = useState([{}])
    const [trashList, setTrashList] = useState([{}])
    const [title, setTitle] = useState('')
    const [desc, setDesc] = useState('')

  useEffect(() => {
    axios.get('http://localhost:8001/api/todo')
      .then(res => {
        setTodoList(res.data)
      })
  }, []);

    useEffect(() => {
    axios.get('http://localhost:8001/api/trashbin')
      .then(res => {
        setTrashList(res.data)
      })
  }, []);

  const addTodoHandler = () => {
    axios.post('http://localhost:8001/api/todo/', { 'title': title, 'description': desc })
      .then(res => console.log(res))
  }

  return (
    <div className="App">
      <h1>Add new TODO</h1>
      <input onChange={event => setTitle(event.target.value)} placeholder='Title' /> <input onChange={event => setDesc(event.target.value)} placeholder='Description' /><button onClick={addTodoHandler}>Add</button>
      <h2>Todo List</h2>
      <TodoListView todoList={todoList} />
      <h2>Trash List</h2>
      <TrashBinView trashList={trashList}/>
    </div>
  );
}

export default App;