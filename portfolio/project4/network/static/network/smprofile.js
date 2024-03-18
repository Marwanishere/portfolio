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
