const diskMap: string = await getInput();
const parsedDiskMap: string[] = parseDiskContents(diskMap, 0);

const formattedDiskMethodA: string[] = moveIndividualFiles(parsedDiskMap);
const formattedDiskMethodB: string[] = moveWholeFiles(parsedDiskMap);

console.log(calculateChecksum(formattedDiskMethodA));
console.log(calculateChecksum(formattedDiskMethodB));

function moveIndividualFiles(parsedDisk: string[]): string[] {
    const tempDisk: string[] = structuredClone(parsedDisk);

    let storagePointer: number = 0;
    let movePointer: number = tempDisk.length - 1;

    while (storagePointer !== movePointer) {
        if (tempDisk[movePointer] === ".") {
            movePointer--;
            continue;
        }

        if (tempDisk[storagePointer] === ".") {
            tempDisk[storagePointer] = tempDisk[movePointer];
            tempDisk[movePointer] = ".";
        }

        storagePointer++;
    }

    return tempDisk;
}

function moveWholeFiles(parsedDisk: string[]): string[] {
    const tempDisk: string[] = structuredClone(parsedDisk);

    let storagePointer: number = 0;
    let movePointer: number = tempDisk.length - 1;

    let fileID: string;
    let fileIDCount: number = 0;

    let freeSpace: number = 0;

    let canMoveLeft: boolean = true;

    while (movePointer !== 0) {
        if (canMoveLeft) {
            fileID = tempDisk[movePointer];

            if (fileID === ".") {
                movePointer--;
                continue;
            }

            while (tempDisk[movePointer] === fileID) {
                fileIDCount++;
                movePointer--;

                if (!movePointer) {
                    break;
                }
            }
            canMoveLeft = false;
        }

        if (tempDisk[storagePointer] === ".") {
            freeSpace++;
            while (tempDisk[storagePointer + 1] === ".") {
                freeSpace++;
                storagePointer++;

                if (storagePointer >= tempDisk.length) {
                    break;
                }
            }

            if (storagePointer > movePointer) {
                storagePointer = 0;
                fileIDCount = 0;
                freeSpace = 0;
                canMoveLeft = true;
                continue;
            }

            if (freeSpace >= fileIDCount) {
                for (let i = freeSpace - 1; i >= 0; i--) {
                    if (!fileIDCount) {
                        break;
                    }

                    tempDisk[storagePointer - i] = tempDisk[movePointer + fileIDCount];
                    tempDisk[movePointer + fileIDCount] = ".";

                    fileIDCount--;
                }
            }

            freeSpace = 0;
        }

        storagePointer++;
    }

    return tempDisk;
}

function calculateChecksum(parsedDisk: string[]): number {
    let total: number = 0;

    for (let blockPos = 0; blockPos <= parsedDisk.length - 1; blockPos++) {
        if (parsedDisk[blockPos] === ".") {
            continue;
        }

        total += blockPos * parseInt(parsedDisk[blockPos]);
    }

    return total;
}

function parseDiskContents(disk: string, currID: number): string[] {
    const parsedDisk: string[] = [];
    let numOfBlocks: number;
    let fileBlock: string;
    let freeSpaces: string;

    for (let i = 0; i <= disk.length - 1; i++) {
        numOfBlocks = Number(disk[i]);

        if (i % 2 == 0) {
            fileBlock = currID.toString();
            for (let j = 1; j <= numOfBlocks; j++) {
                parsedDisk.push(fileBlock);
            }

            currID++;
            continue;
        }

        freeSpaces = ".".repeat(numOfBlocks);
        for (const freeSpace of freeSpaces) {
            parsedDisk.push(freeSpace);
        }
    }

    return parsedDisk;
}

async function getInput(): Promise<string> {
    const buffer = new Uint8Array(1048576);
    const bytesRead = await Deno.stdin.read(buffer);
    const rawText: string = new TextDecoder().decode(buffer.slice(0, bytesRead!));

    return rawText.trim();
}
