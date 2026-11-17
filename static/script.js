
// =====================================
// 映画一覧を取得する関数（GET）
// =====================================
async function getMovies() {
    try {
        const response = await fetch("/api/movies");

        if (!response.ok) {
            throw new Error("映画の取得に失敗しました");
        }

        const movies = await response.json();

        displayMovies(movies);

    } catch (error) {
        console.error("エラーが発生しました：", error);

        const movieList = document.getElementById("movie-list");
        movieList.textContent = "映画情報を取得できませんでした。";
    }
}


// =====================================
// 映画一覧をHTMLに表示する関数
// =====================================
function displayMovies(movies) {

    const movieList = document.getElementById("movie-list");

    movieList.replaceChildren();

    if (movies.length === 0) {
        movieList.textContent = "映画が登録されていません。";
        return;
    }

    movies.forEach(movie => {

        const movieItem = document.createElement("div");
        movieItem.classList.add("movie-card");

        // 映画タイトル
        const title = document.createElement("h3");
        title.textContent = movie.title;

        // 監督
        const director = document.createElement("p");
        director.textContent = "監督：" + movie.director;

        // ジャンル
        const genre = document.createElement("p");
        genre.textContent = "ジャンル：" + movie.genre;

        // 公開年
        const year = document.createElement("p");
        year.textContent = "公開年：" + movie.year;

        // 評価
        const rating = document.createElement("p");
        rating.textContent = "評価：" + movie.rating + " / 5";

        // 編集ボタン
        const editButton = document.createElement("button");
        editButton.textContent = "編集";
        editButton.type = "button";

        editButton.addEventListener("click", function() {
            editMovie(movie);
        });

        // 削除ボタン
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "削除";
        deleteButton.type = "button";

        deleteButton.addEventListener("click", function() {
            deleteMovie(movie.id);
        });

        // 映画情報を追加
        movieItem.appendChild(title);
        movieItem.appendChild(director);
        movieItem.appendChild(genre);
        movieItem.appendChild(year);
        movieItem.appendChild(rating);
        movieItem.appendChild(editButton);
        movieItem.appendChild(deleteButton);

        movieList.appendChild(movieItem);
    });
}


// =====================================
// 映画の新規登録（POST）
// =====================================

const movieForm = document.getElementById("movie-form");

movieForm.addEventListener("submit", async function(event) {

    // 通常のフォーム送信を防ぐ
    event.preventDefault();

    // 入力された映画情報を取得
    const movieData = {
        title: document.getElementById("title").value.trim(),
        director: document.getElementById("director").value.trim(),
        genre: document.getElementById("genre").value.trim(),
        year: Number(document.getElementById("year").value),
        rating: Number(document.getElementById("rating").value)
    };

    const message = document.getElementById("message");

    try {
        const response = await fetch("/api/movies", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(movieData)
        });

        if (!response.ok) {
            throw new Error("映画の登録に失敗しました");
        }

        message.textContent = "映画を登録しました。";

        // フォームをリセット
        movieForm.reset();

        // 映画一覧を更新
        await getMovies();

    } catch (error) {
        message.textContent = error.message;
        console.error("エラーが発生しました：", error);
    }
});


// =====================================
// 映画情報を編集フォームに表示する
// =====================================

function editMovie(movie) {

    // 編集フォームを表示
    document.getElementById("edit-section").style.display = "block";

    // 映画IDを保存
    document.getElementById("edit-id").value = movie.id;

    // 現在の映画情報を入力欄に表示
    document.getElementById("edit-title").value = movie.title;
    document.getElementById("edit-director").value = movie.director;
    document.getElementById("edit-genre").value = movie.genre;
    document.getElementById("edit-year").value = movie.year;
    document.getElementById("edit-rating").value = movie.rating;

    // 編集フォームまで移動
    document.getElementById("edit-section").scrollIntoView({
        behavior: "smooth"
    });
}


// =====================================
// 映画情報の更新（PUT）
// =====================================

const editForm = document.getElementById("edit-form");

editForm.addEventListener("submit", async function(event) {

    // 通常のフォーム送信を防ぐ
    event.preventDefault();

    // 編集対象の映画IDを取得
    const movieId = document.getElementById("edit-id").value;

    // 編集後の映画情報を取得
    const movieData = {
        title: document.getElementById("edit-title").value.trim(),
        director: document.getElementById("edit-director").value.trim(),
        genre: document.getElementById("edit-genre").value.trim(),
        year: Number(document.getElementById("edit-year").value),
        rating: Number(document.getElementById("edit-rating").value)
    };

    try {
        const response = await fetch(`/api/movies/${movieId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(movieData)
        });

        if (!response.ok) {
            throw new Error("映画情報の更新に失敗しました");
        }

        // 編集フォームをリセット
        editForm.reset();

        // 編集フォームを非表示
        document.getElementById("edit-section").style.display = "none";

        // 映画一覧を更新
        await getMovies();

        alert("映画情報を更新しました。");

    } catch (error) {
        console.error("エラーが発生しました：", error);
        alert(error.message);
    }
});


// =====================================
// 編集のキャンセル
// =====================================

document.getElementById("cancel-edit").addEventListener("click", function() {

    // 編集フォームを非表示
    document.getElementById("edit-section").style.display = "none";

    // 入力内容をリセット
    editForm.reset();
});


// =====================================
// 映画の削除（DELETE）
// =====================================

async function deleteMovie(movieId) {

    // 削除前に確認
    const confirmed = confirm("この映画を削除しますか？");

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(`/api/movies/${movieId}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("映画の削除に失敗しました");
        }

        // 映画一覧を更新
        await getMovies();

    } catch (error) {
        console.error("エラーが発生しました：", error);
        alert(error.message);
    }
}


// =====================================
// 最初に映画一覧を取得する
// =====================================

getMovies();
