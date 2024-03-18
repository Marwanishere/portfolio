document.addEventListener('DOMContentLoaded', function() {
    console.log("JavaScript finally working")
    document.querySelector('#submit-post').onclick = (e) => {
        e.preventDefault()
        // has to be something another var up top is preventDefault is a method of the event object, not the document object.
        // You should modify your event handler to receive an event parameter and call preventDefault on that.
        const title = document.querySelector('#title-content').value;
        const content = document.querySelector('#post-content').value;
        console.log("submit button clicked")
        // fetch request below changed in line with cs50 chatbot hint
        fetch('/npost', {
            method: 'POST',
            headers: {
                // line below used in conjunction with getCookie function to solve techical issue, acquired 
                // through cs50 chatbot prompting
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                title: title,
                content: content
            })
        })
        console.log(` just to make sure the logging has been done correctly here is the title: ${title}`)
        location.reload()
        // reload function gets rid of all console.log in this coument.queryselector area, line above acquired through cs50 prompting
    }
})
// function below acquired from cs50 chatbot and is purely there to solve a techincal issue 403 error
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// below query selector acquired by cs50 chatbot
document.querySelectorAll('#delete-button').forEach(button => {
    button.addEventListener('click', delete_old_post);
});
// below function skeleton/body made using cs50 chatbot then adapted to fit use case
function delete_old_post(e) {
    e.preventDefault()
    let id = e.target.dataset.id;
    console.log(`Deleted post with id ${id}`)
    fetch(`/delete_post/${id}/`, {
        method: 'DELETE',
        headers: {
            // line below used in conjunction with getCookie function to solve techical issue, acquired 
            // through cs50 chatbot prompting
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            id: id
        })
    })
    .finally(()=> location.reload());
}
document.querySelectorAll('#edit-button').forEach(button => {
    button.addEventListener('click', edit_post);
});
document.querySelectorAll('#save-button').forEach(button => {
    button.addEventListener('click', save_post);
});
function edit_post(e){
    e.preventDefault()
    e.target.style.display = 'None';
    var id = e.target.dataset.id;
    var sb = document.querySelector(`#save-button[data-id= '${id}']`);
    sb.style.display = 'block';    
    console.log(`the id of the selected post is '${id}'`)
    var ta = document.querySelector(`#text-area[data-id = '${id}']`)
    ta.style.display = 'block';
    let ot = document.querySelector(`#original-text[data-id = '${id}']`).textContent;
    document.querySelector(`#text-area[data-id = '${id}']`).value = ot;
    document.querySelector(`#original-text[data-id = '${id}']`).style.display = 'none';
}
function save_post(e){
    e.preventDefault()
    e.target.style.display = 'None';
    var id = e.target.dataset.id;
    var eb = document.querySelector(`#edit-button[data-id= '${id}']`);
    eb.style.display = 'block'; 
    console.log(`the id of the selected post is '${id}'`)
    var ta = document.querySelector(`#text-area[data-id = '${id}']`)
    ta.style.display = 'None';
    fetch(`/edit_post/${id}`,{
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body:JSON.stringify({
            content: ta.value,
            id: id
        })
    })
    .then(r => r.json())
    .then(newer => { document.querySelector(`#original-text[data-id = '${id}']`).textContent = newer.content;
    document.querySelector(`#original-text[data-id = '${id}']`).style.display = 'block';})
    .finally(()=> location.reload());
}
document.querySelectorAll('#unlike-button').forEach(button => {
    button.addEventListener('click', unlike_post);
});
document.querySelectorAll('#like-button').forEach(button => {
    button.addEventListener('click', like_post);
});

function unlike_post(e){
    e.preventDefault()
    e.target.style.display = "None"
    var id = e.target.dataset.id;
    var lb = document.querySelector(`#like-button[data-id= '${id}']`);
    lb.style.display = 'inline';
    liked = true;
    fetch(`/liked_post/${id}`,{
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body:JSON.stringify({
            liked: liked,
            id: id
        })
    })
    .then(r => r.json())
}
function like_post(e){
    e.preventDefault()
    e.target.style.display = "None"
    var id = e.target.dataset.id;
    var ulb = document.querySelector(`#unlike-button[data-id= '${id}']`);
    ulb.style.display = 'inline';
    liked = false;
    fetch(`/liked_post/${id}`,{
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body:JSON.stringify({
            liked: liked,
            id: id
        })
    })
    .then(r => r.json())
}
