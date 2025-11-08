const borderedPuzzle: string[][] = await getInput();

type Coordinates = [number, number];

const validHikingTrails: number = countValidHikingPaths(borderedPuzzle, findAllStartingTrails(borderedPuzzle), true);
const validDistinctHikingTrails: number = countValidHikingPaths(
    borderedPuzzle,
    findAllStartingTrails(borderedPuzzle),
    false
);

console.log(validHikingTrails);
console.log(validDistinctHikingTrails);

function findAllStartingTrails(trail: string[][]): Coordinates[] {
    const startingTrails: Coordinates[] = [];
    for (let i = 1; i < trail.length - 1; i++) {
        for (let j = 1; j < trail[i].length - 1; j++) {
            if (trail[i][j] === "0") {
                startingTrails.push([i, j]);
            }
        }
    }

    return startingTrails;
}

function countValidHikingPaths(trail: string[][], startPositions: Coordinates[], markEndOfTrail: boolean): number {
    function helper(currHeight: number, yPos: number, xPos: number): void {
        for (const direction of directions) {
            if (plotTrail[yPos][xPos] === "9") {
                if (markEndOfTrail) {
                    plotTrail[yPos][xPos] = "P";
                }
                validHikingPathsCount++;
                break;
            }

            if (plotTrail[yPos + direction[0]][xPos + direction[1]] === (currHeight + 1).toString()) {
                helper(currHeight + 1, yPos + direction[0], xPos + direction[1]);
            }
        }
    }

    let plotTrail: string[][];
    const directions: Coordinates[] = [
        [0, -1],
        [0, 1],
        [-1, 0],
        [1, 0],
    ];
    let validHikingPathsCount: number = 0;

    for (const startPosition of startPositions) {
        plotTrail = structuredClone(trail);
        helper(0, startPosition[0], startPosition[1]);
    }

    return validHikingPathsCount;
}

function addPuzzleBorders(arr: string[]): string[][] {
    const puzzleWithBorders: string[][] = [];

    if (arr.length == 0) {
        throw "Array is empty.";
    }

    const horizontalBorder: string = "*".repeat(arr[0].length + 2);

    puzzleWithBorders.push([...horizontalBorder]);

    for (let i = 0; i < arr.length; i++) {
        puzzleWithBorders.push([...("*" + arr[i] + "*")]);
    }

    puzzleWithBorders.push([...horizontalBorder]);

    return puzzleWithBorders;
}

async function getInput(): Promise<string[][]> {
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
