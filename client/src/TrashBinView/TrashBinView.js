import React from 'react';
import axios from 'axios'
import DeletedTodo from "../DeletedTodo/DeletedTodo";


export default function TrashBinView(props) {
    const deleteAllHandler = () => {
        axios.delete('http://localhost:8001/api/trash-bin/')
            .then(res => {
                console.log(res)
                window.location.reload()
            })
    }
    return (
        <div>
            <ul>
                {props.trashList.map(todo => <DeletedTodo todo={todo} />)}
                <button onClick={deleteAllHandler} style={{ color: 'red' }}>Delete All</button>
            </ul>
        </div>
    )
}