const fs = require('fs');
const ytdl = require('ytdl-core');
const path = require('path');

function format_time(seconds){
    seconds = parseInt(seconds);
    if (seconds < 60 * 60){
        seconds = `${Math.floor(seconds / 60)}:${(seconds % 60).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false})}`;
    } else {
        seconds = `${Math.floor(seconds / 60 / 60)}:${Math.floor(seconds % (60 * 60) / 60).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false})}:${(seconds % (60 * 60) % 60).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false})}`;
    }
    return seconds;
}

function format_title(title){
    let illegal_chars = ["#", "<", ">", "$", "+", "%", "!", "`", "&", "*", "\'", "\"", "|",
    "{", "}", "/", "\\", ":", "@"]

    return new Promise((resolve, reject) => {
        if(typeof title != "undefined"){
            // only resolve the promise if title is defined
            illegal_chars.forEach((char) => {
                title = title.replace(char, "-");
            });
            resolve(title);
        }
    });
}

// function format_title(title){
//     let illegal_chars = ["#", "<", ">", "$", "+", "%", "!", "`", "&", "*", "\'", "\"", "|",
//     "{", "}", "/", "\\", ":", "@"]

//     if(typeof title != "undefined"){
//         illegal_chars.forEach((char) => {
//             title = title.replace(char, "-");
//         });
//         resolve(title);
//     }
// }

async function get_info(url){
    console.log("[Wait] Fetching info.");
    const info = await ytdl.getBasicInfo(url);
    const thumbnails = info.videoDetails.thumbnails;
    console.log("Done");
    return {
        title: info.videoDetails.title,
        download: JSON.stringify({url: url, filename: await format_title(info.videoDetails.title)}),
        timestamp: format_time(info.videoDetails.lengthSeconds),
        views: info.response.contents.twoColumnWatchNextResults.results.results.contents[0].videoPrimaryInfoRenderer.viewCount.videoViewCountRenderer.shortViewCount.simpleText,
        thumbnail: thumbnails[thumbnails.length - 1].url
    }
}

function downloadVideo(url, filename){
    console.log(`[Downloading] ${filename}.mp4`);
    let file_path = path.join(__dirname+"/video", filename+".mp4")
    return new Promise(async (resolve, reject)=>{
        await ytdl(url).pipe(fs.createWriteStream(file_path)).on("finish", () => {
            console.log("Done");
            resolve(file_path); // Return the file path
        });        
    });
}

function downloadAudio(url, filename){
    console.log(`[Downloading] ${filename}.mp3`);
    let file_path = path.join(__dirname+"/audio", filename+".mp3")
    return new Promise(async (resolve, reject)=>{
        await ytdl(url, {quality: 'highestaudio', filter: 'audioonly' })
        .pipe(fs.createWriteStream(file_path)).on("finish", () => {
            console.log("Done");
            resolve(file_path); // Return the file path
        });        
    });
}

exports.get_info = get_info;
exports.downloadAudio = downloadAudio;
exports.downloadVideo = downloadVideo;

async function main(){
    // await downloadVideo("https://youtu.be/dQw4w9WgXcQ", "Rickroll.mp4")
    // .then(() => console.log("Done"));
    // await ytdl("http://www.youtube.com/watch?v=aqz-KE-bpKQ").pipe(fs.createWriteStream("Rickroll.mp4"));
    // const info = await ytdl.getBasicInfo("http://www.youtube.com/watch?v=aqz-KE-bpKQ");
    // const thumbnails = info.videoDetails.thumbnails
    // const video_details = {
    //     title: info.videoDetails.title,
    //     timestamp: info.videoDetails.lengthSeconds,
    //     views: info.response.contents.twoColumnWatchNextResults.results.results.contents[0].videoPrimaryInfoRenderer.viewCount.videoViewCountRenderer.shortViewCount.simpleText,
    //     thumbnail: thumbnails[thumbnails.length - 1].url
    //     }
    // console.log(typeof info.player_response.frameworkUpdates.entityBatchUpdate.timestamp.seconds);
    // let data = JSON.stringify(info);
    // fs.writeFileSync('data.json', data);
    const url = "https://youtu.be/dQw4w9WgXcQ";
    const meta = await get_info(url);
    console.log(meta);
    // console.log(await downloadVideo(url, JSON.parse(meta.download).filename));
    // console.log(await downloadAudio(url, JSON.parse(meta.download).filename));
}

if (require.main == module) {
    //console.log(__dirname);
    main();
}