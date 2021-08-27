const express = require("express");
const ytbe = require(__dirname+"/YouTube.js");

const app = express();
app.set("view engine", "ejs");
const port = 3000;
app.use(express.urlencoded({extended: true}));
app.use(express.static("public"));

app.get("/", function(req, res){
    res.render("index");
});

app.post("/show", async function(req, res){
    try{
        let url = req.body.url;
        const meta = await ytbe.get_info(url);
        console.log(meta);
        res.render("show", meta);
    }
    catch (e){
        res.sendFile(__dirname + "/failure.html");
    }
});

app.post("/download", async function(req, res){
    try {
        const format = req.body.format;
        const download = JSON.parse(req.body.Download);
        const url  = download.url;
        const filename = download.filename;
        let file = "";
        console.log(`${format} ${url} ${filename}`);

        if (format == "mp3"){
            file = await ytbe.downloadAudio(url, filename);
        } else {
            file = await ytbe.downloadVideo(url, filename);
        }

        res.download(file);
    }
    catch (e){
        res.sendFile(__dirname + "/failure.html");
    }
});

app.post("/failure", function(req, res){
    res.redirect("/");
});

app.listen(process.env.PORT || port, function(){
    console.log(`App listening at http://localhost:${port}`);
});