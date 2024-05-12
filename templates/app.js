document.querySelectorAll('.nav-link').forEach(item => {
    item.addEventListener('mouseover', event => {
        switch (event.target.innerText) {
            case 'Movies':
                document.getElementById('body').style.backgroundImage = 'url("movies.jpg")';
                break;
            case 'Songs':
                document.getElementById('body').style.backgroundImage = 'url("songs.avif")';
                break;
            case 'Books':
                document.getElementById('body').style.backgroundImage = 'url("books.jpg")';
                break;
        }
    })

    item.addEventListener('mouseout', event => {
        document.getElementById('body').style.backgroundImage = 'none';
    })
})