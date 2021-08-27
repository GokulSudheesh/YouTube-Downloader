const fs = require("fs/promises");
const path = require('path');

function del (){
    const dirs = ["audio", "video"];
    try {
        dirs.forEach(async (element) => {
            const dir = await fs.opendir(element);
            for await (const dirent of dir)
                await fs.rm(path.join(element, dirent.name));
        });
        
    } catch (err) {
        console.error(err);
    }
}

del();