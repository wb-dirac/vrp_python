/**
 * Created by wb on 15-12-6.
 */
function renderSortedOrders(SortedOrders, map){
    SortedOrders = JSON.parse(SortedOrders);
    for(var carNum in SortedOrders){
        var car = SortedOrders[carNum]
        var color = getRandomColor();
        var sharp = getRandomSharp();
        for(var i in car) {
            var point = car[i]
            //设置marker图标为水滴
            var vectorMarker = new BMap.Marker(new BMap.Point(point.longitude, point.latitude), {
                // 指定Marker的icon属性为Symbol
                icon: new BMap.Symbol(sharp, {
                    scale: 1,//图标缩放大小
                    fillColor: color,//填充颜色
                    fillOpacity: 1//填充透明度
                })
            });

            map.addOverlay(vectorMarker);
        }
    }
}

function getRandomColor(){
    return '#'+Math.floor(Math.random()*16777215).toString(16);
}

function getRandomSharp(){

    var sharps = [BMap_Symbol_SHAPE_STAR, BMap_Symbol_SHAPE_WARNING, BMap_Symbol_SHAPE_CLOCK, BMap_Symbol_SHAPE_POINT];
    return sharps[Math.floor(Math.random() * sharps.length)];
}

function renadOrigin(point, map){
    var vectorMarker = new BMap.Marker(point, {
                // 指定Marker的icon属性为Symbol
                icon: new BMap.Symbol(BMap_Symbol_SHAPE_POINT, {
                    scale: 1.5,//图标缩放大小
                    fillColor: "red",//填充颜色
                    fillOpacity: 1//填充透明度
                })
            });

    map.addOverlay(vectorMarker);
}

function initMap(id, centerPoint){

    var map = new BMap.Map(id);
    map.centerAndZoom(centerPoint, 12);
    map.enableScrollWheelZoom(true);
    return map;
}

function renderPath(orderSet, cars, startPoint, map){
    var count = 0;
    for(var carNum in cars){
        var orders = cars[carNum]
        var color = getRandomColor();
        var sharp = getRandomSharp();
        var points = [startPoint];

        for(var i in orders) {
            count++;
            var point = orderSet[orders[i]]
            //设置marker图标为水滴
            var mapPoint = new BMap.Point(point.lng, point.lat);
            points.push(mapPoint);
            var vectorMarker = new BMap.Marker(mapPoint, {
                // 指定Marker的icon属性为Symbol
                icon: new BMap.Symbol(sharp, {
                    scale: 1,//图标缩放大小
                    fillColor: color,//填充颜色
                    fillOpacity: 1//填充透明度
                })
            });

            map.addOverlay(vectorMarker);
        }
        var polyline = new BMap.Polyline(points, {strokeColor:color, strokeWeight:1, strokeOpacity:0.5});   //创建折线
        map.addOverlay(polyline);
    }
    console.log(count);
}