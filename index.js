// ユーザーのテーブルセルを取得する
const getUserCell = (user) => {
    const name = user ? user.name : '';
    const screenName = user ? user.screen_name : '';
    const userCell = $('<td>', { class: 'text-truncate' });
    const link = screenName ? `https://twitter.com/${screenName}` : '';
    const anchor = $('<a>', link ? { href: link, target: '_blank', text: name } : { text: name });
    $(userCell).append(anchor);
    return userCell;
};

// ツイートのテーブルセルを取得する
const getTweetCell = (tweet) => {
    const shorten = (text) => text.replace(/https:[^\s]+$/, '').trim();
    const tweetId = tweet ? tweet.id_str : '';
    const text = tweet ? shorten(tweet.text) : '';
    const link = tweetId ? `https://twitter.com/Twitter/status/${tweetId}` : '';
    const tweetCell = $('<td>', { class: 'text-truncate' });
    const anchor = $('<a>', link ? { href: link, target: '_blank', text: text } : { text: text });
    $(tweetCell).append(anchor);
    return tweetCell;
};

// 日時のテーブルセルを取得する
const getTimeCell = (timestamp, tweet) => {
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
    const tweetId = tweet ? tweet.id_str : '';
    const link = tweetId ? `https://twitter.com/Twitter/status/${tweetId}` : '';
    const timeCell = $('<td>', { class: 'text-truncate' });
    const anchor = $('<a>', link ? { href: link, target: '_blank', text: dateString } : { text: dateString });
    $(timeCell).append(anchor);
    return timeCell;
};

// 通知を表示する
const showNotice = (notice) => {
    const tableRow = $('<tr>');
    $(tableRow).append(getUserCell(notice.receiver));
    $(tableRow).append(getUserCell(notice.sender));
    $(tableRow).append(getTweetCell(notice.tweet));
    $(tableRow).append(getTimeCell(notice.timestamp, notice.tweet));
    $('tbody').append(tableRow);
};

// メイン処理
const main = (noticeUrl, receiverId) => {
    $.ajax({
        url: noticeUrl + '/notices',
        type: 'GET',
        dataType: 'json',
        data: { receiver_id: receiverId, size: 100, mode: 'expand' }
    })
    .then(
        notices => {
            $('table').removeClass('d-none');
            $('tbody').empty();
            notices.forEach((notice) => showNotice(notice));
        },
        error => console.error(error)
    );
};

// ロードイベント
$(document).ready(() => {
    const noticeUrl = localStorage.getItem('NOTICE_API_URL');
    const receiverId = localStorage.getItem('RECEIVER_ID');
    if (noticeUrl && receiverId) main(noticeUrl, receiverId);
});

// クリックイベント: 設定ボタン
$(document).on('click', '#setting', () => {
    const noticeUrl = localStorage.getItem('NOTICE_API_URL');
    const receiverId = localStorage.getItem('RECEIVER_ID');
    $('#noticeUrl').val(noticeUrl);
    $('#receiverId').val(receiverId);
});

// クリックイベント: 更新ボタン
$(document).on('click', '#update', () => {
    const noticeUrl = $('#noticeUrl').val();
    const receiverId = $('#receiverId').val();
    localStorage.setItem('NOTICE_API_URL', noticeUrl);
    localStorage.setItem('RECEIVER_ID', receiverId);
    main(noticeUrl, receiverId);
});
