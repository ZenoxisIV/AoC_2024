const borderedPuzzle: string[] = await getInput();
const nodeMap: string[][] = [];

type Coordinates = [number, number];
const antinodesLocations: Coordinates[] = [];
const harmonizedAntinodesLocations: Coordinates[] = [];

for (let i = 0; i < borderedPuzzle.length; i++) {
    nodeMap.push(borderedPuzzle[i].split(""));
}

for (let i = 1; i < nodeMap.length - 1; i++) {
    for (let j = 1; j < nodeMap[i].length - 1; j++) {
        if (nodeMap[i][j] === ".") {
            continue;
        }

        let p: number;
        let q: number;

        for (let k = 1; k <= Math.min(nodeMap.length, nodeMap[0].length); k++) {
            p = 1;
            while (nodeMap[i][j - p] !== "*") {
                q = 1;
                while (nodeMap[i + q][j - p] !== "*") {
                    if (nodeMap[i][j] === nodeMap[i + q][j - p]) {
                        if (k === 1) {
                            getValidAntinodesLocations(
                                antinodesLocations,
                                nodeMap,
                                [i, j],
                                [i + q, j - p],
                                p,
                                q,
                                "LEFT"
                            );
                        }

                        if (!hasCoordinates(harmonizedAntinodesLocations, [i, j])) {
                            harmonizedAntinodesLocations.push([i, j]);
                        }
                        if (!hasCoordinates(harmonizedAntinodesLocations, [i + q, j - p])) {
                            harmonizedAntinodesLocations.push([i + q, j - p]);
                        }
                        getValidAntinodesLocations(
                            harmonizedAntinodesLocations,
                            nodeMap,
                            [i, j],
                            [i + q, j - p],
                            k * p,
                            k * q,
                            "LEFT"
                        );
                    }
                    q += 1;
                }
                p += 1;
            }

            p = 1;
            while (nodeMap[i][j + p] !== "*") {
                q = 1;
                while (nodeMap[i + q][j + p] !== "*") {
                    if (nodeMap[i][j] === nodeMap[i + q][j + p]) {
                        if (k === 1) {
                            getValidAntinodesLocations(
                                antinodesLocations,
                                nodeMap,
                                [i, j],
                                [i + q, j + p],
                                p,
                                q,
                                "RIGHT"
                            );
                        }

                        if (!hasCoordinates(harmonizedAntinodesLocations, [i, j])) {
                            harmonizedAntinodesLocations.push([i, j]);
                        }
                        if (!hasCoordinates(harmonizedAntinodesLocations, [i + q, j + p])) {
                            harmonizedAntinodesLocations.push([i + q, j + p]);
                        }
                        getValidAntinodesLocations(
                            harmonizedAntinodesLocations,
                            nodeMap,
                            [i, j],
                            [i + q, j + p],
                            k * p,
                            k * q,
                            "RIGHT"
                        );
                    }
                    q += 1;
                }
                p += 1;
            }
        }
    }
}

console.log(antinodesLocations.length);
console.log(harmonizedAntinodesLocations.length);

function getValidAntinodesLocations(
    nodeLocs: Coordinates[],
    nodeMap: string[][],
    nodePosA: readonly [number, number],
    nodePosB: readonly [number, number],
    spanP: number,
    spanQ: number,
    mode: string
): void {
    let yFinalPosA: number;
    let xFinalPosA: number;

    let yFinalPosB: number;
    let xFinalPosB: number;

    switch (mode) {
        case "LEFT": {
            yFinalPosA = nodePosA[0] - spanQ;
            xFinalPosA = nodePosA[1] + spanP;

            yFinalPosB = nodePosB[0] + spanQ;
            xFinalPosB = nodePosB[1] - spanP;

            break;
        }

        case "RIGHT": {
            yFinalPosA = nodePosA[0] - spanQ;
            xFinalPosA = nodePosA[1] - spanP;

            yFinalPosB = nodePosB[0] + spanQ;
            xFinalPosB = nodePosB[1] + spanP;

            break;
        }

        default: {
            throw "Unknown mode.";
        }
    }

    const yBound: number = nodeMap.length;
    const xBound: number = nodeMap[0].length;

    if (isInbound(yBound, xBound, yFinalPosA, xFinalPosA)) {
        const nodeA: [number, number] = [yFinalPosA, xFinalPosA];
        if (!hasCoordinates(nodeLocs, nodeA)) {
            nodeLocs.push(nodeA);
        }
    }
    if (isInbound(yBound, xBound, yFinalPosB, xFinalPosB)) {
        const nodeB: [number, number] = [yFinalPosB, xFinalPosB];
        if (!hasCoordinates(nodeLocs, nodeB)) {
            nodeLocs.push(nodeB);
        }
    }
}

function isInbound(yBound: number, xBound: number, yPos: number, xPos: number): boolean {
    // Note: '*' added borders are considered out of bounds
    return 1 <= yPos && yPos < yBound - 1 && 1 <= xPos && xPos < xBound - 1;
}

function hasCoordinates(arr: Coordinates[], target: Coordinates): boolean {
    return arr.some(([y, x]) => y === target[0] && x === target[1]);
}

function addPuzzleBorders(arr: string[]): string[] {
    const puzzleWithBorders: string[] = [];

    if (arr.length == 0) {
        throw "Array is empty.";
    }

    const horizontalBorder: string = "*".repeat(arr[0].length + 2);

    puzzleWithBorders.push(horizontalBorder);

    for (let i = 0; i < arr.length; i++) {
        puzzleWithBorders.push("*" + arr[i] + "*");
    }

    puzzleWithBorders.push(horizontalBorder);

    return puzzleWithBorders;
}

async function getInput(): Promise<string[]> {
    const buffer = new Uint8Array(8192);

    while (true) {
        const bytesRead = await Deno.stdin.read(buffer);

        if (bytesRead === null) {
            break;
        }
    }

    const rawText: string = new TextDecoder().decode(buffer);
    const puzzle: string[] = rawText.split("\n");

    puzzle.pop(); // remove null terminating string

    return addPuzzleBorders(puzzle);
}
