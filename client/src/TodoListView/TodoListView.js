import React from 'react';
import Todo from '../Todo/Todo'
import axios from 'axios'


export default function TodoListView(props) {
    const deleteAllHandler = () => {
        axios.delete('http://localhost:8001/api/todo/')
            .then(res => {
                console.log(res)
                window.location.reload() // Refresh the page
            })
    }
    return (
        <div>
            <ul>
                {props.todoList.map(todo => <Todo todo={todo} />)}
                <button onClick={deleteAllHandler} style={{ color: 'red' }}>Delete All</button>
            </ul>
        </div>
    )
}