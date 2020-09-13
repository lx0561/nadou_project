// 外部js文件
$(function() {
    function roomdata(data) {
        var html = '';
        $.each(data, function(i, o) {
                // 刘先生的家是个变量,需要从跳转前的页面获取roomname来对比js里面的roomname
                if (o.roomtitle == "原创设计森林系树屋大床房/全实木/春熙路/太古里/九眼桥/兰桂坊-A") {
                    var room = `<div class="rooms">
            <h3 class="roomtitle">
                <a href="#">${o.roomtitle}</a>
            </h3>
            <ul>
                <li class="type">
                    <div></div>
                    <a href="#">${o.roomtype.type}</a>
                </li>
                <li class="bed">
                    <a href="#">${o.roomtype.bed}</a>
                </li>
                <li class="toilet">
                    <a href="#">${o.roomtype.toilet}</a>
                </li>
            </ul>
            <p class="roomname">
                ${o.roomname}
            </p>
            <p class="phone">
                ${o.phone}
            </p>
            <p class="roomtext">
                ${o.roomtext}
            </p>
        </div>
        `
                    html += room;
                }
            })
            // 将拼接好的字符串追加到页面
        $('.roombox').append(html);
        console.log(html)
    }
    res = roomdata(roomData)
    console.log(res)
})