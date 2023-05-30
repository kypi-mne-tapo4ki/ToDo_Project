import React from 'react';
import Todo from '../Todo/Todo'
import axios from 'axios'


export default function TrashBinView(props) {
    const deleteAllHandler = () => {
        axios.delete('http://localhost:8001/api/trashbin/')
            .then(res => {
                console.log(res)
                window.location.reload() // Refresh the page
            })
    }
    return (
        <div>
            <ul>
                {props.trashList.map(todo => <Todo todo={todo} />)}
                <button onClick={deleteAllHandler} style={{ color: 'red' }}>Delete All</button>
            </ul>
        </div>
    )
}