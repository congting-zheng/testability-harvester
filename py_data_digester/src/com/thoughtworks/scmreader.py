from com.thoughtworks.core import *
from pysvn import *

class SCMReader:
    
    # Return Value: List of ChangeSet
    def changeSets(self, proPath):
        pass
    
    # Return Value: String
    def cat(self, projectPath, filePath, revision):
        pass
    
    # Return Value: Diff
    def diff(self, projectPath, filePath, sourceRevisionNumber, targetRevisionNumber):
        pass


class SVNReader(SCMReader):
    def __init__(self):
        self.client = Client()

    def changeSets(self, proPath):
        logger.info("SVNReader.changeSets - Start loading changesets from SVN...")
        logMessages = self.client.log(proPath, discover_changed_paths=True)
        logger.info("SVNReader.changeSets - Finish loading changesets from SVN...")
        
        logger.info("SVNReader.changeSets - Start Parsing ChangeSets...")
        changeSets = self.parseLogToChangeSets(logMessages, proPath)
        logger.info("SVNReader.changeSets - Finish Parsing ChangeSets...")
        
        return changeSets
    
    def cat(self, projectPath, filePath, revision):
        logger.info("SVNReader.cat - Start concatenating " + filePath + " from SVN...")
        fileContent = self.client.cat(projectPath + filePath, Revision(opt_revision_kind.number, revision))
        logger.info("SVNReader.cat - Finish concatenating " + filePath + " from SVN...")
        
        return fileContent
    
    def diff(self, projectPath, filePath, sourceRevisionNumber, targetRevisionNumber):
        temp_prefix = "./temp_diff_"
        
        revisionStart = Revision(opt_revision_kind.number, sourceRevisionNumber)
        logger.info("SVNReader.diff - revisionStart: " + revisionStart)
        
        revisionEnd = Revision(opt_revision_kind.number, targetRevisionNumber)
        logger.info("SVNReader.diff - revisionEnd: " + revisionEnd)
        
        logger.info("SVNReader.diff - Start loading diffs from SVN...")
        diffContent = self.client.diff(temp_prefix, projectPath + filePath, revision1=revisionStart, revision2=revisionEnd)
        logger.info("SVNReader.diff - Finish loading diffs from SVN...")
        
        diff = Diff()
        diff.content = diffContent
        
        return diff
    
    def parseLogToChangeSets(self, logMessages, proPath):
        length = len(logMessages)
        counter = 0
        changeSets = []
        for logMessage in logMessages:
            counter += 1
            if counter == length:
                author = 'Null'
            else:
                author = logMessage["author"]
            date = str(logMessage["date"])
            revision = logMessage["revision"].number
            changedpaths = logMessage["changed_paths"]
            files = self.parseChangedpathToFiles(changedpaths)
            
            changeSets.append(ChangeSet(revision, author, date, files, proPath))
        return changeSets
    
    def parseChangedpathToFiles(self, changedpaths):
        files = []
        for changedpath in changedpaths:
            path = changedpath["path"][len("M /trunk") - 1:]
            action = changedpath["action"] 
            files.append(self.createFile(action, path))
        return files
    
    def createFile(self, action, path):
        if action == 'A':
            file = AddedFile(path)
        elif action == 'D':
            file = DeletedFile(path)
        elif action == 'M':
            file = ModifiedFile(path)
        return file


class SCMReaderStub(SCMReader):
    
    def changeSets(self, proPath):
        return []
    
    def cat(self, projectPath, filePath, revision):
        return ''
    
    def diff(self, projectPath, filePath, sourceRevisionNumber, targetRevisionNumber):
        return ''
