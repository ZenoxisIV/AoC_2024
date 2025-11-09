const initialStones: number[] = await getInput();

console.log(countStones(initialStones, 25));
console.log(countStones(initialStones, 75));

function countStones(stones: number[], blinks: number): number {
    const stoneCache: Record<string, number> = {};

    function blink(stone: number, remainingBlinks: number): number {
        const key = `${stone},${remainingBlinks}`;
        
        if (stoneCache[key] !== undefined) {
            return stoneCache[key];
        }

        if (remainingBlinks === 0) {
            return 1;
        }

        let stoneCount: number;

        if (stone === 0) {
            stoneCount = blink(1, remainingBlinks - 1);
        } else {
            const s = stone.toString();
            if (s.length % 2 === 0) {
                const leftStone = parseInt(s.slice(0, s.length / 2), 10);
                const rightStone = parseInt(s.slice(s.length / 2), 10);
                stoneCount = blink(leftStone, remainingBlinks - 1) + blink(rightStone, remainingBlinks - 1);
            } else {
                stoneCount = blink(stone * 2024, remainingBlinks - 1);
            }
        }

        stoneCache[key] = stoneCount;
        return stoneCount;
    }

    return stones.reduce((sum, stone) => sum + blink(stone, blinks), 0);
}

async function getInput(): Promise<number[]> {
    const buffer = new Uint8Array(1024);
    const bytesRead = await Deno.stdin.read(buffer);
    const rawText: string = new TextDecoder().decode(buffer.slice(0, bytesRead!));
    
    return rawText.trim().split(" ").map(Number);
}
