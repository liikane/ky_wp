// Example JavaScript file with syntax errors fixed

function processData(data) {
    let result = [];
    
    for (let i = 0; i < data.length; i++) {
        if (data[i].active) {
            result.push({
                id: data[i].id,
                name: data[i].name,
                value: data[i].value
            });
        } // Fixed: This brace correctly closes the if statement
    } // This brace closes the for loop correctly
    
    return result;
} // Fixed: Added closing brace for function

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];
    }
    
    addData(item) {
        this.data.push(item);
    }
    
    process() {
        return this.data.map(item => {
            return {
                ...item,
                processed: true
            };
        });
    } // Fixed: Added closing brace for method
} // Fixed: Added closing brace for class

const processor = new DataProcessor({ debug: true });
processor.addData({ id: 1, name: "Test", active: true });

console.log(processor.process());