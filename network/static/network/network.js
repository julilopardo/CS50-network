
function like(id) {
  var like_btn= document.querySelector(`#like-btn-${id}`);
  var like_count= document.querySelector(`#like-count-${id}`);

  //Like    
    if(like_btn.style.color == 'darkgray') {
      like_btn.style.color = 'red';

      fetch('/like/' + id, {
        method: 'PUT',
        body: JSON.stringify({
          like: true
        })
      })

      fetch('/like/'+ id)
      .then(response => response.json())
      .then(data => {
        likes= data.likes;
        like_count.innerHTML = `${likes} likes(s)`;
      })     
    }

  //Unlike    
    else {
      like_btn.style.color = 'darkgray';

      fetch('/like/' + id, {
        method: 'PUT',
        body: JSON.stringify({
          like: false
        })
      })    

      fetch('/like/' + id)
      .then(response => response.json())
      .then(data => {
        likes= data.likes;
        like_count.innerHTML = `${likes} likes(s)`;
      })
    }

    return false;

}

function follow(user) {
  var follow_btn = document.querySelector(`#follow_button-${user}`);
  var follow_count = document.querySelector('#followers');
  var action = follow_btn.innerHTML;
    
    //Follow
    if (action == "Follow") {
      follow_btn.innerHTML= "Unfollow";

      fetch('/follow/'+ user, {
        method: 'PUT',
        body: JSON.stringify({
          follow: true
        })
      })

      fetch('/follow/' + user)
      .then(response => response.json())
      .then(data => {
        num_of_followers= data.followers;
        follow_count.innerHTML = `${num_of_followers} Followers`;
      });
    }

    //Unfollow    
    if (action == "Unfollow") {
      follow_btn.innerHTML= "Follow";

      fetch('/follow/'+ user, {
        method: 'PUT',
        body: JSON.stringify({
          follow: false
        })
      })

      fetch('/follow/' + user)
      .then(response => response.json())
      .then(data => {
        num_of_followers= data.followers;
        follow_count.innerHTML =  `${num_of_followers} Followers`;
      });
        
    }
    return false;
}

function edit(id) {
  //Show edit elements (button and textarea)
  var edit_box= document.querySelector(`#edit-box-${id}`);
  edit_box.style.display= 'block';
  var edit_btn= document.querySelector(`#edit-btn-${id}`);
  edit_btn.style.display= 'block';

  //Hide post to edit
  var current_post = document.querySelector(`#post-content-${id}`);
  current_post.style.display='none';

  //On click edit_btn run 'edit' on views.py with the json response as inputs 
  edit_btn.addEventListener('click', () => {
    fetch('/edit/' + id, {
      method: 'PUT',
      body: JSON.stringify({
        post: edit_box.value
      })
    });

    //Hide edit elemments
    edit_box.style.display= 'none';
    edit_btn.style.display= 'none';

    //Change content of post
    document.querySelector(`#post-content-${id}`).innerHTML= edit_box.value;

    //Show post again
    current_post.style.display='block';

  });

}