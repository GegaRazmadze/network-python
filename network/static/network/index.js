document.addEventListener('DOMContentLoaded', function() {
    // set like button inner HTML
    document.querySelectorAll('.like_button').forEach(element => {
        set_like_button(element);
    })

    // Event Listener for Form   
    document.querySelectorAll('.post_form').forEach(element => {
        element.addEventListener('submit', function(event) {
            event.preventDefault();
        })
    })
    // Event Listener for Button
    document.querySelectorAll('.edit_button').forEach(element => {
        element.addEventListener('click', edit_post)
    })

    // like Post Function
    document.querySelectorAll('.like_form').forEach(element => {
        element.addEventListener('submit', function(event) {
        event.preventDefault();
        likeFunction(element);
        })
    })
   
});



function  set_like_button(element) {
    user = parseInt(element.dataset.user);
    post_id = element.dataset.post;
    likes = element.dataset.likes;

    like_button = document.querySelector(`#like_button_${post_id}`);

    // string to array
    likes = eval(likes)

    user_like = likes.find(x => x.id === user);

    if (Boolean(user_like)) {
        like_button.innerHTML = 'UnLike'
    } else {
        like_button.innerHTML = 'Like'
    }
}
    


function edit_post() {
    post_id = this.dataset.post;
    //select
    post_form = document.querySelector(`#post_form${post_id}`);

    post_button = document.querySelector(`#button_${post_id}`);

    button_name = post_button.innerHTML;

    post_textarea = document.querySelector(`#post_body${post_id}`);

    

    if (button_name === 'Edit') {
        post_button.innerHTML = 'Save';
        // change texarea bihevior
        post_textarea.disabled = false;
    } else {
        post_button.innerHTML = 'Edit';
        // text value:
        body = post_form.elements[`textarea_${post_id}`].value;

        // Update Post body:
        fetch(`/edit_post/${post_id}`, {
          method: 'PUT',
          body: JSON.stringify({
              body: body
          })
        })
        // change texarea bihevior  
        post_textarea.disabled = true;
    }
}

function likeFunction(element) {
    const post_id = element.id
    const like_button = document.querySelector(`#like_button_${post_id}`)
    let like_button_text = like_button.innerHTML
    // To eliminate spaces
    let trim = like_button_text.trim()

    let res;
    const likes = document.querySelector(`#like_count_${post_id}`)

    // to int
    const trimCount = parseInt(likes.innerHTML)

    form = new FormData();
    form.append("post_id", post_id);

    fetch('/like_post/', {
        method: 'POST',
        body: form,
    })
    .then((res) => {
        console.log(res)

        if (trim === 'UnLike') {
            like_button.innerHTML = 'Like';
            res = trimCount - 1
        } else {
            like_button.innerHTML = 'UnLike';
            res = trimCount + 1
        }
        likes.innerHTML = res;
    })
    .catch(err => console.log(err))
}
