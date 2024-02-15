import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('extension.plotGraph', () => {
        // Prompt the user for input
        vscode.window.showInputBox({ prompt: 'Enter the plot description' }).then((description) => {
            if (description) {
                const pythonScriptPath = context.asAbsolutePath('src/script.py');
                const pythonExecutablePath = 'python'; // Ensure this points to the correct Python executable
                const command = `"${pythonExecutablePath}" "${pythonScriptPath}" "${description}"`;

                exec(command, (err, stdout, stderr) => {
                    if (err) {
                        vscode.window.showErrorMessage('Error executing Python script: ' + stderr);
                        return;
                    }

                    // Create a new document with the generated code
                    vscode.workspace.openTextDocument({ content: stdout, language: 'python' })
                        .then(doc => vscode.window.showTextDocument(doc))
                        .then(editor => {
                            // Save the document to a temporary file
                            const tempFilePath = path.join(context.extensionPath, 'temp.py');
                            fs.writeFile(tempFilePath, stdout, (err) => {
                                if (err) {
                                    vscode.window.showErrorMessage('Failed to save the temporary plot file.');
                                    return;
                                }

                                // Execute the plot code in the integrated terminal
                                let terminal = vscode.window.terminals.find(t => t.name === "Python Plot") || vscode.window.createTerminal("Python Plot");
                                terminal.show();
                                terminal.sendText(`python "${tempFilePath}"`);
                            });
                        });
                });
            }
        });
    });

    context.subscriptions.push(disposable);
}
