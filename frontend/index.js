// ユーザーのテーブルセルを取得する
const getUserCell = (user) => {
    const name = user ? user.name : '';
    const screenName = user ? user.screen_name : '';
    const userCell = $('<td>', { class: 'text-truncate' });
    const link = `https://twitter.com/${screenName}`;
    const anchor = $('<a>', { href: link, target: '_blank', text: name });
    $(userCell).append(anchor);
    return userCell;
};

// ツイートのテーブルセルを取得する
const getTweetCell = (tweet) => {
    const shorten = (text) => text.replace(/https:[^\s]+$/, '').trim();
    const tweetId = tweet ? tweet.id_str : '';
    const text = tweet ? shorten(tweet.text) : '';
    const tweetCell = $('<td>', { class: 'text-truncate' });
    const link = `https://twitter.com/Twitter/status/${tweetId}`;
    const anchor = $('<a>', { href: link, target: '_blank', text: text });
    $(tweetCell).append(anchor);
    return tweetCell;
};

// 日時のテーブルセルを取得する
const getTimeCell = (timestamp) => {
    const getDateString = (date) => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, 0);
        const day = String(date.getDate()).padStart(2, 0);
        const hour = String(date.getHours()).padStart(2, 0);
        const min = String(date.getMinutes()).padStart(2, 0);
        return `${year}-${month}-${day} · ${hour}:${min}`;
    };
    const dateTime = new Date(timestamp * 1000);
    const dateString = getDateString(dateTime);
    const timeCell = $('<td>', { class: 'text-truncate' });
    const anchor = $('<a>', { text: dateString });
    $(timeCell).append(anchor);
    return timeCell;
};

// 通知を表示する
const showNotice = (notice) => {
    const tableRow = $('<tr>');
    $(tableRow).append(getUserCell(notice.receiver));
    $(tableRow).append(getUserCell(notice.sender));
    $(tableRow).append(getTweetCell(notice.tweet));
    $(tableRow).append(getTimeCell(notice.timestamp));
    $('tbody').append(tableRow);
};

// メイン処理
const doMainProcess = (url) => {
    $('#URLSubmit').prop('disabled', true);
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        data: { size: 100, mode: 'expand' }
    })
    .then(
        notices => notices.forEach((notice) => showNotice(notice)),
        error => console.error(error)
    )
    .then(
        () => $('#URLSubmit').prop('disabled', false)
    );
};

// ロード
$(document).ready(() => {
    const url = localStorage.getItem('NOTICE_API_URL');
    if (url) doMainProcess(url);
});

// クリックイベント on 更新ボタン
$(document).on('click', '#URLSubmit', () => {
    const url = $('#URLInput').val();
    $('#URLInput').val('');
    localStorage.setItem('NOTICE_API_URL', url);
    doMainProcess(url);
});
