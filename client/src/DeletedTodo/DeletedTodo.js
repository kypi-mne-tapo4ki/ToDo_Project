import axios from 'axios'
import React from 'react'
import moment from 'moment'

export default function DeletedTodo(props) {
    const deleteTodoHandler = (title) => {
        axios.delete(`http://localhost:8001/api/trash-bin/${title}`)
            .then(res => {
                console.log(res)
                window.location.reload()
            })
    }
    const restoreTodoHandler = (title) => {
        axios.post(`http://localhost:8001/api/todo/`, { 'title': props.todo.title, 'description': props.todo.description })
            .then(res => {
                deleteTodoHandler(title)
                console.log(res)
                window.location.reload()
            })
    }
    const date = moment(props.todo.time);
    const formattedDate = date.format('H:mm DD-MM-YYYY');
    return (
        <div style={{ display: "flex", justifyContent: 'center' }}>
            <div style={{ width: "500px" }}>
                <p>
                    <span style={{ fontWeight: 'bold' }}>{props.todo.title}:</span> {props.todo.description}  |  (deleted at {formattedDate})
                    <button onClick={() => deleteTodoHandler(props.todo.title)} style={{ color: 'red' }}>Delete</button>
                    <button onClick={() => restoreTodoHandler(props.todo.title)} style={{ color: 'green' }}>Restore</button>
                </p>
            </div>
        </div>
    )
}